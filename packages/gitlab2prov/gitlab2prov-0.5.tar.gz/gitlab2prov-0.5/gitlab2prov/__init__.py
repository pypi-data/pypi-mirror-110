"""Extract provenance from GitLab projects."""

__author__ = "Claas de Boer, Andreas Schreiber"
__copyright__ = "Copyright 2020, German Aerospace Center (DLR) and individual contributors"
__license__ = "MIT"
__version__ = "0.5"
__status__ = "Development"

import asyncio

from collections import namedtuple, defaultdict
from typing import List, Optional, Type, Tuple

from prov.model import ProvDocument, PROV_REC_CLS, ProvActivity, ProvEntity, ProvAgent, ProvRelation, ProvElement
from prov.identifier import QualifiedName
from prov.dot import prov_to_dot

from gitlab2prov.models import enforce_uniqueness_constraints
from gitlab2prov.api import GitlabClient
from gitlab2prov.pipelines import CommitPipeline, CommitResourcePipeline, IssueResourcePipeline, MergeRequestResourcePipeline, ReleaseTagPipeline
from gitlab2prov.utils import q_name, url_encoded_path


class Gitlab2Prov:

    def __init__(self, token, rate=10, git_commits=True, gitlab_commits=True, issues=True, merge_requests=True):
        """Initialize with api token, api rate limit and pipeline configuration."""
        self.token = token
        self.rate = rate
        self.pipelines = [
            CommitPipeline(),
            CommitResourcePipeline(),
            IssueResourcePipeline(),
            MergeRequestResourcePipeline(),
            ReleaseTagPipeline()
        ]

    def compute_graph(self, url):
        """Compute graph for gitlab project at *url*."""
        graphs = self.run_pipelines(url)
        graph = self.unite_graphs(graphs)
        graph = self.postprocess(graph, url)
        graph = self.unite_agents(graph, alias_map={})
        return graph

    def unite_graphs(self, graphs):
        """Unite graphs by updating accumulator with records from others."""
        acc = graphs[0]
        for sub_graph in graphs[1:]:
            acc.update(sub_graph)
        graph = enforce_uniqueness_constraints(acc)
        return graph

    def run_pipelines(self, url: str) -> List[ProvDocument]:
        """Run Pipelines for a given client."""
        client = GitlabClient(url, self.token, self.rate)
        graphs = []
        for pipe in self.pipelines:
            data = asyncio.run(pipe.fetch(client))
            packages = pipe.process(*data)
            graphs.append(pipe.create_model(packages))
        return graphs

    def postprocess(self, graph, url):
        """Prepend project identifier to identifiers of activities and entities.
        Add project identifier to node attributes of activities and entities."""
        records = list(graph.get_records(ProvAgent))
        id_map = {agent.identifier: agent.identifier for agent in records}
        project = url_encoded_path(url).replace("%2F", "/")

        for record in graph.get_records((ProvActivity, ProvEntity)):
            attributes = [*record.attributes, *record.formal_attributes]
            attributes.append(("project", project))

            identifier = record.identifier
            namespace, localpart = identifier.namespace, identifier.localpart
            unique_id = QualifiedName(namespace, q_name(f"{project}-{localpart}"))
            id_map[identifier] = unique_id

            if isinstance(record, ProvEntity):
                records.append(ProvEntity(record.bundle, unique_id, attributes))
            else:
                records.append(ProvActivity(record.bundle, unique_id, attributes))

        records.extend(graph.get_records(ProvRelation))
        graph = ProvDocument(records)
        graph = self.update_relations(graph, id_map)
        return graph

    def update_relations(self, graph, id_map):
        """Update start and enpoints of relations according to node id mapping."""
        records = list(graph.get_records(ProvElement))
        for relation in graph.get_records(ProvRelation):
            (s_type, s), (t_type, t) = relation.formal_attributes[:2]

            attributes = [(s_type, id_map.get(s, s)), (t_type, id_map.get(t, t))]
            attributes.extend(relation.formal_attributes[2:])
            attributes.extend(relation.extra_attributes)

            r_type = PROV_REC_CLS[relation.get_type()]
            records.append(r_type(relation.bundle, relation.identifier, attributes))

        return ProvDocument(records)

    def unite_agents(self, graph, alias_map):
        """Unite agents that represent the same person based on their aliases."""
        records = list(graph.get_records((ProvActivity, ProvEntity)))
        id_map = {}
        agents = defaultdict(list)
        for agent in graph.get_records(ProvAgent):
            n_key, name = {k.localpart: (k, v) for k, v in agent.attributes}["name"]
            name = alias_map.get(name, name)

            agents[name].extend(agent.attributes)
            agents[name].extend(agent.formal_attributes)
            agents[name] = [(k, v) for k, v in agents[name] if k != n_key]
            agents[name].append((n_key, name))

            id_ = QualifiedName(agent.identifier.namespace, q_name(f"user-{name}"))
            id_map[agent.identifier] = id_
            records.append(ProvAgent(agent.bundle, id_, agents[name]))

        records.extend(graph.get_records(ProvRelation))
        graph = ProvDocument(records)
        graph = self.update_relations(graph, id_map)
        return graph

    def pseudonymize(self, graph):
        """Pseudonymize agents by replacing their name by a number.
        Remove all other agent attribute information."""
        records = list(graph.get_records((ProvActivity, ProvEntity, ProvRelation)))
        for code_name, agent in enumerate(set(graph.get_records(ProvAgent))):
            attributes = {k.localpart: (v, k) for k, v in agent.attributes}
            attributes = {attributes["name"][1]: str(code_name)}
            records.append(ProvAgent(agent.bundle, agent.identifier, attributes))
        graph = ProvDocument(records)
        return graph
