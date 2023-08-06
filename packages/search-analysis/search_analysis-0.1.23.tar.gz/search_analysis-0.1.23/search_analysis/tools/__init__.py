import collections
import csv
from collections import OrderedDict, defaultdict
import warnings
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
import json
import re


class EvaluationObject:
    def __init__(self, host, query_rel_dict, index, name, verified_certificates=False):
        self.queries_rels = dict(query_rel_dict)
        self.index = index
        self.name = name
        if verified_certificates:
            self.elasticsearch = Elasticsearch([host])
        else:
            self.elasticsearch = Elasticsearch([host], ca_certs=False, verify_certs=verified_certificates, read_timeout=120)
        self.elasticsearch.ping()
        self.true_positives = {}
        self.false_positives = {}
        self.false_negatives = {}
        self.recall = {}
        self.precision = {}
        self.fscore = {}
        # orange, green, turquoise, black, red, yellow, white
        self.pragma_colors = ['#ffb900', '#8cab13', '#22ab82', '#242526', '#cc0000', '#ffcc00', '#ffffff']

    def _check_size(self, k, size):
        """
        Checking `size` argument; size needs to be >= k.

        Parameters
        ----------
        :arg k: int
            ranking size
        :arg size: int or None
            search size, if size is None, it will set Elastisearch default value

        :Returns:
        -------

        :size: int
            adjusted search size

        """
        if size is not None:
            if size < k:
                size = k
        return size

    def _get_search_result(self, query_id, size, fields):
        """
        Sends a search request for every query to Elasticsearch and returns the result including highlighting.

        Parameters
        ----------
        :arg query_id: int
            current query id
        :arg size: int
            search size
        :arg fields: list of strings
            fields that should be searched on

        :Returns:
        -------
        :result: nested dict
            search result from Elasticsearch

        """
        body = self._get_highlights_search_body(self.queries_rels[query_id]['question'], size, fields)
        result = self.elasticsearch.search(index=self.index, body=body)
        return result

    def _get_highlights_search_body(self, query, size=20, fields=["text", "title"]):
        """
        Creates a search body with the highlights option to return a highlighted search result.

        Parameters
        ----------
        :arg query: str
            query to search on
        :arg size: int
            searched size
        :arg fields: list of str
            fields, that should be searched

        :Returns:
        -------
        search body for highlighting the matched results

        """
        return {
            "size": size,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": fields
                }
            },
            "highlight": {
                "fields": {
                    "*": {}
                }
            }
        }

    def _check_searched_queries(self, query_ids):
        """
        Checks if query_ids is an int or None and transforms it to a list.
        If it's None, all available queries are used for the search.

        Parameters
        ----------
        :arg query_ids: list, int or None

        :Returns:
        -------
        :query_ids: list
            transformed query ids

        """
        if type(query_ids) == int:
            query_ids = [query_ids]
        if query_ids is None:
            query_ids = [*self.queries_rels]
        return query_ids

    def _create_hit(self, pos, hit, fields):
        """
        Creates a structured dict of the hit from Elasticsearch.

        Parameters
        ----------
        :arg pos: int or str,
            ranking position
        :arg hit: nested dict
            hit found in Elasticsearch
        :arg fields: list of strings
            fields so analyze

        :Returns:
        -------
        :variable: nested dict
            structured hit

        """
        doc_fields = {}
        highlights = {}
        for curr_field in fields:
            try:
                doc_fields[curr_field] = hit["_source"][curr_field]
                if curr_field in hit["highlight"].keys():
                    highlights[curr_field] = hit["highlight"][curr_field]
            except KeyError:
                continue

        variable = {
            "position": pos,
            "score": hit["_score"],
            "doc": {"id": int(hit["_id"])},
            "highlight": {}
        }
        for field_name, highlight in highlights.items():
            variable["highlight"][field_name] = highlight
        for field, data in doc_fields.items():
            variable["doc"][field] = data
        return variable

    def _initialize_distributions(self, searched_queries=None, fields=['text', 'title'], size=20, k=20):
        """
        Gets distributions and saves them in self.true_positives, self.false_positives and self.false_negatives.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            query ids; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            number of results that should be returned and ranked

        Returns
        -------

        """
        size = self._check_size(k, size)
        searched_queries = self._check_searched_queries(searched_queries)
        self.true_positives = self.get_true_positives(searched_queries, fields, size, k, False)
        self.false_positives = self.get_false_positives(searched_queries, fields, size, k, False)
        self.false_negatives = self.get_false_negatives(searched_queries, fields, size, k, False)

    def _calculate_recall(self, tp, fn):
        """
        Calculates Recall.

        https://en.wikipedia.org/wiki/Precision_and_recall

        Parameters
        ----------
        :arg tp: int
            true positives
        :arg fn: int
            false negatives

        :Returns:
        -------
        Recall value

        """
        if (tp + fn) == 0:
            warnings.warn('Sum of true positives and false negatives is 0. Please check your data, '
                          'this shouldn\'t happen. Maybe you tried searching on the wrong index, with the wrong '
                          'queries or on the wrong fields.')
            return 0
        return tp / (tp + fn)

    def _calculate_precision(self, tp, fp):
        """
        Calculates Precision.

        https://en.wikipedia.org/wiki/Precision_and_recall

        Parameters
        ----------
        :arg tp: int
            true positives
        :arg fp: int
            false positives

        :Returns:
        -------
        Precision value

        """
        if (tp + fp) == 0:
            warnings.warn('Sum of true positives and false positives is 0. Please check your data, '
                          'this shouldn\'t happen. Maybe you tried searching on the wrong index, with the wrong '
                          'queries or on the wrong fields.')
            return 0
        return tp / (tp + fp)

    def _calculate_fscore(self, precision, recall, factor=1):
        """
        Calculates F-Score.

        https://en.wikipedia.org/wiki/F-score

        Parameters
        ----------
        :arg precision: int
            precision value
        :arg recall: int
            recall value
        :arg factor: int or float
            1 is the default to calculate F1-Score, but you can also choose another factor

        :Returns:
        -------
        F-Score value

        """
        if recall or precision != 0:
            if factor is 1:
                return (2 * precision * recall) / (precision + recall)
            else:
                return (1 + factor ** 2) * ((precision * recall) / (factor ** 2 * precision + recall))
        else:
            warnings.warn('The value of precision and/or recall is 0.')
            return 0

    def get_true_positives(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False):
        """
        Calculates true positives from given search queries.


        Parameters
        ----------
        :arg searched_queries: int or list or None
            query ids; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it returns json

        :Returns:
        -------

        :true positives: json

        """
        size = self._check_size(k, size)
        searched_queries = self._check_searched_queries(searched_queries)
        # initializing dictionary of true positives;
        true_pos = {}
        for query_ID in searched_queries:
            true_pos["Query_" + str(query_ID)] = {
                "question": self.queries_rels[query_ID]['question'],
                "true_positives": []
            }
            result = self._get_search_result(query_ID, size, fields)
            for pos, hit in enumerate(result["hits"]["hits"], start=1):
                # check if `hit` IS a relevant document; in case `hits` position < k, it counts as a true positive;
                if int(hit["_id"]) in self.queries_rels[query_ID]['relevance_assessments'] and pos <= k:
                    true = self._create_hit(pos, hit, fields)
                    true_pos["Query_" + str(query_ID)]["true_positives"].append(true)
        if dumps:
            return json.dumps(true_pos, indent=4)
        else:
            return true_pos

    def get_false_positives(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False):
        """
        Calculates false positives from given search queries.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            query ids; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it returns json

        :Returns:
        -------

        :false positives: json

        """
        size = self._check_size(k, size)
        searched_queries = self._check_searched_queries(searched_queries)
        # initializing dictionary of false positives;
        false_pos = {}
        for query_ID in searched_queries:
            false_pos["Query_" + str(query_ID)] = {
                "question": self.queries_rels[query_ID]['question'],
                "false_positives": []
            }
            result = self._get_search_result(query_ID, size, fields)
            # for every `hit` in the search results... ;
            for pos, hit in enumerate(result["hits"]["hits"], start=1):
                # check if `hit` IS a relevant document; in case `hits` position < k, it counts as a true positive;
                if int(hit["_id"]) not in self.queries_rels[query_ID]['relevance_assessments'] and pos < k:
                    false = self._create_hit(pos, hit, fields)
                    false_pos["Query_" + str(query_ID)]["false_positives"].append(false)
        if dumps:
            return json.dumps(false_pos, indent=4)
        else:
            return false_pos

    def get_false_negatives(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False):
        """
        Calculates false negatives from given search queries.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            query ids; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it returns json

        :Returns:
        -------

        :false negatives: json

        """
        size = self._check_size(k, size)
        searched_queries = self._check_searched_queries(searched_queries)
        # initializing dictionary of false negatives;
        false_neg = {}
        for query_ID in searched_queries:
            false_neg["Query_" + str(query_ID)] = {
                "question": self.queries_rels[query_ID]['question'],
                "false_negatives": []
            }
            result = self._get_search_result(query_ID, size, fields)
            # iterating through the results;
            query_rel = self.queries_rels[query_ID]['relevance_assessments'].copy()
            for pos, hit in enumerate(result["hits"]["hits"], start=1):
                # false negatives require that the result belongs to the relevance assessments;
                if int(hit["_id"]) in query_rel:
                    if pos > k:
                        # create a `false negative`;
                        false = self._create_hit(pos, hit, fields)
                        # save `false hit/positive`;
                        false_neg["Query_" + str(query_ID)]["false_negatives"].insert(0, false)
                        # removes the `hit` from the remaining relevant documents;
                    query_rel.remove(int(hit["_id"]))
            # adds all missing relevant docs to the start of the `false negatives` with `position = -1`;
            for relevant_doc in query_rel:
                # create a `false negative`;
                false = {
                    "position": -1,
                    "score": None,
                    "doc": {
                        "id": relevant_doc
                    }
                }
                false_neg["Query_" + str(query_ID)]["false_negatives"].insert(0, false)
        if dumps:
            return json.dumps(false_neg, indent=4)
        else:
            return false_neg

    def get_recall(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False):
        """
        Calculates recall for every search query given.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            searched queries; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it saves to object variable

        :Returns:
        -------

        json with Recall values

        """
        if not self.true_positives:
            self._initialize_distributions(searched_queries, fields, size, k)
        true_pos = self.count_distribution('true_positives', self.true_positives, False, k)
        false_neg = self.count_distribution('false_negatives', self.false_negatives, False, k)
        recall = defaultdict(dict)
        recall_sum = 0.0
        for query, data in true_pos.items():
            if not query == 'total':
                recall_value = self._calculate_recall(true_pos[query]['count'], false_neg[query]['count'])
                recall[query]['recall'] = recall_value
                recall_sum += recall_value
        recall = OrderedDict(sorted(recall.items(), key=lambda i: i[1]['recall']))
        recall['total'] = (recall_sum / len(self.queries_rels))
        if dumps:
            return json.dumps(recall, indent=4)
        else:
            self.recall = recall

    def get_precision(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False):
        """
        Calculates precision for every search query given.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            searched queries; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it saves to object variable

        :Returns:
        -------

        json with Precision values

        """
        if not self.true_positives:
            self._initialize_distributions(searched_queries, fields, size, k)
        true_pos = self.count_distribution('true_positives', self.true_positives, False, k)
        false_pos = self.count_distribution('false_positives', self.false_positives, False, k)
        precision = defaultdict(dict)
        precision_sum = 0.0
        for query, data in true_pos.items():
            if not query == 'total':
                precision_value = self._calculate_precision(true_pos[query]['count'], false_pos[query]['count'])
                precision[query]['precision'] = precision_value
                precision_sum += precision_value
        precision = OrderedDict(sorted(precision.items(), key=lambda i: i[1]['precision']))
        precision['total'] = (precision_sum / len(self.queries_rels))
        if dumps:
            return json.dumps(precision, indent=4)
        else:
            self.precision = precision

    def get_fscore(self, searched_queries=None, fields=['text', 'title'], size=20, k=20, dumps=False, factor=1):
        """
        Calculates f-score for every search query given.

        Parameters
        ----------
        :arg searched_queries: int or list or None
            searched queries; if None it searches with all queries
        :arg fields: list of str
            fields that should be searched on
        :arg size: int
            search size
        :arg k: int
            top results that should be returned from Elasticsearch
        :arg dumps: True or False
            if True it returns json.dumps, if False it saves to object variable
        :arg factor: int
            can be used to weight the F score, default is 1

        :Returns:
        -------

        json with F-score values

        """
        if not self.recall:
            self.get_recall(searched_queries, fields, size, k, False)
        if not self.precision:
            self.get_precision(searched_queries, fields, size, k, False)
        fscore = defaultdict(dict)
        for query, data in self.precision.items():
            if not query == 'total':
                fscore_value = self._calculate_fscore(self.precision[query]['precision'], self.recall[query]['recall'],
                                                      factor)
                fscore[query]['fscore'] = fscore_value
        fscore = OrderedDict(sorted(fscore.items(), key=lambda i: i[1]['fscore']))
        fscore['total'] = self._calculate_fscore(self.precision['total'], self.recall['total'], factor)
        if dumps:
            return json.dumps(fscore, indent=4)
        else:
            self.fscore = fscore

    def count_distribution(self, distribution, distribution_json, dumps=False, k=20):
        """
        Counts given distribution per query, relevant documents and calculates percentages given the relevant documents.

        Parameters
        ----------
        :arg distribution: string
            'true_positives', 'false_positives' or 'false_negatives'
        :arg distribution_json: json
            json with all the distributions needed; e.g. EvaluationObject.true_positives
        :arg dumps: True or False
            if True it returns json.dumps, if False it returns json
        :arg k: int
            size of k top search results

        :Returns:
        ---------
            :sorted_counts: json
                    counted distribution per query, as a sum and as a percentage

        """
        if isinstance(distribution_json, str):
            result_json = json.loads(distribution_json)
        else:
            result_json = distribution_json
        counts = defaultdict(dict)
        sum_rels = 0
        sum_count = 0
        for query in result_json:
            query_id = int(query.strip('Query_'))
            count_query = int(len(result_json[query][distribution]))
            count_rels = int(len(self.queries_rels[query_id]['relevance_assessments']))
            if distribution == 'false_positives':
                f = k - count_query
                if f == count_rels or count_rels == 0:
                    percentage = 0
                else:
                    percentage = (count_rels - f) * 100 / count_rels
            else:
                if count_rels == 0:
                    percentage = 0
                else:
                    percentage = (100 * count_query / count_rels)
            counts[query] = {'count': count_query, 'percentage': percentage, 'relevant documents': count_rels}
            sum_rels += count_rels
            sum_count += count_query
        if distribution == 'false_positives':
            f = (k * len(counts)) - sum_count
            if f == sum_rels or sum_rels == 0:
                sum_percentage = 0
            else:
                sum_percentage = (sum_rels - f) * 100 / sum_rels
        else:
            if sum_rels == 0:
                sum_percentage = 0
            else:
                sum_percentage = (100 * sum_count / sum_rels)
        sorted_counts = OrderedDict(sorted(counts.items(), key=lambda i: i[1]['percentage']))
        sorted_counts['total'] = {'total sum': sum_count, 'percentage': str(sum_percentage) + '%'}
        if dumps:
            return json.dumps(sorted_counts, indent=4)
        else:
            return sorted_counts

    def explain_query(self, query_id, doc_id, fields=['text', 'title'], dumps=True):
        """
        Returns an Elasticsearch explanation for given query and document.

        https://www.elastic.co/guide/en/elasticsearch/reference/current/search-explain.html

        Parameters
        ----------
        :arg query_id: int
            id of query that should be explained
        :arg doc_id: int
            id of document that should be explained
        :arg fields: list of str
            fields that should be searched on
        :arg dumps: True or False
            True by default, if False it won't convert dict to json

        :Returns:
        -------

        json or dict explaining query and document match
        """
        query_body = {
            "query": {
                "multi_match": {
                    "fields": fields,
                    "query": self.queries_rels[query_id]['question']
                }
            }
        }
        explain = defaultdict(lambda: defaultdict(lambda: []))
        explanation = self.elasticsearch.explain(self.index, doc_id, query_body)['explanation']
        explain["score"] = explanation['value']
        if explain["score"] == 0.0:
            print('No hits with that request, please check all the parameters like index, fields, query dictionary, '
                  'etc.')
            return explanation
        if explanation['description'] != "max of:":
            explanation = {'details': [explanation]}

        for el in explanation['details']:
            field = ''.join(f for f in fields if re.search(f, el['details'][0]['description']))
            explain[field]["total_value"] = el['details'][0]['value']
            explain[field]["details"] = []
            for detail in el['details']:
                doc_freq = 0
                term_freq = 0.0
                for val in detail['details'][0]["details"]:
                    try:
                        if re.match('n, number of documents', val["details"][0]["description"]):
                            doc_freq = val["details"][0]["value"]
                    except IndexError:
                        continue
                    try:
                        if re.match(r'.*[Ff]req', val["details"][0]["description"]):
                            term_freq = val["details"][0]["value"]
                    except IndexError:
                        continue
                explain[field]["details"].append(
                    {"function": {
                        "value": detail['value'],
                        "description": detail['description'],
                        "n, number of documents containing term": doc_freq,
                        "freq, occurrences of term within document": term_freq}})
        if dumps:
            return json.dumps(explain, indent=4)
        else:
            return explain


class ComparisonTool:
    def __init__(self, host, qry_rel_dict, eval_obj_1=None, eval_obj_2=None,
                 fields=['text', 'title'], index_1=None, index_2=None, name_1='approach_1',
                 name_2='approach_2', size=20, k=20):
        self.qrys_rels = qry_rel_dict
        if eval_obj_1 is None:
            eval_obj_1 = EvaluationObject(host, self.qrys_rels, index_1, name_1)
        if eval_obj_2 is None:
            eval_obj_1 = EvaluationObject(host, self.qrys_rels, index_2, name_2)
        self.eval_obj_1 = eval_obj_1
        self.eval_obj_2 = eval_obj_2
        self.eval_obj_1.get_fscore(None, fields, size, k)
        self.eval_obj_2.get_fscore(None, fields, size, k)
        # orange, green, turquoise, black, red, yellow, white
        self.pragma_colors = ['#ffb900', '#8cab13', '#22ab82', '#242526', '#cc0000', '#ffcc00', '#ffffff']
        self.recall_diffs = {}
        self.precision_diffs = {}
        self.fscore_diffs = {}

    def _get_conditions(self, queries, eval_objs, conditions):
        """
        Gets condition values for the visualization as a pandas data frame.

        Parameters
        ----------
        :arg queries: int or list
            query ids
        :arg eval_objs: list
            EvaluationObjs that should be compared
        :arg conditions: list
            conditions that should be printed

        :Returns:
        -------
        pandas data frame

        """
        vis_dict = defaultdict(list)
        for obj in eval_objs:
            for con in conditions:
                for query in queries:
                    vis_dict['Approach'].append(obj.name)
                    vis_dict['Value'].append(getattr(obj, con)['Query_' + str(query)][con])
                    vis_dict['Scores'].append(con)
        return pd.DataFrame(data=vis_dict)

    def _get_distributions(self, queries, eval_objs, distributions):
        """
        Gets distribution values for the visualization as a pandas data frame.

        Parameters
        ----------
        :arg queries: int or list
            query ids
        :arg eval_objs: list
            EvaluationObjs that should be compared
        :arg distributions: list
            distributions that should be printed

        :Returns:
        -------
        pandas data frame

        """
        dis_dict = defaultdict(list)
        for obj in eval_objs:
            for dist in distributions:
                for query in queries:
                    for el in getattr(obj, dist)['Query_' + str(query)][dist]:
                        dis_dict['Approach'].append(obj.name)
                        dis_dict['Distributions'].append(dist)
        return pd.DataFrame(data=dis_dict)

    def _get_explain_terms(self, query_id, doc_id, fields, eval_objs):
        """
        Returns pandas data frame containing all the found terms and their scores.

        Parameters
        ----------
        :arg query_id: int
            query id of query that should be explained
        :arg doc_id: int
            id of document that should be explained
        :arg fields: list
            fields that should be searched
        :arg eval_objs: list
            EvaluationObjs that should be compared

        :Returns:
        -------
        pandas data frame

        """
        explain_dict = defaultdict(list)
        for obj in eval_objs:
            # explain_dict[obj.name] = defaultdict(list)
            explain = obj.explain_query(query_id, doc_id, fields, dumps=False)
            for field in fields:
                for function in explain[field]['details']:
                    explain_dict['Approach'].append(obj.name)
                    explain_dict['Field'].append(field)
                    explain_dict['Terms'].append(self._extract_terms(function["function"]["description"]))
                    explain_dict['Term Score'].append(function["function"]["value"])
                    explain_dict['Term Frequency per Document'].append(
                        function["function"]["n, number of documents containing term"])
                    explain_dict['Occurrences of Term within Document'].append(
                        function["function"]["freq, occurrences of term within document"])
        # group_counter= 1
        # for terms_1 in explain_dict[eval_objs[0].name]['Terms']:
        #   explain_dict[eval_objs[0].name]['Group'] = group_counter
        #  for eval_obj in eval_objs[1:]:
        #     for terms_2 in explain_dict[eval_obj.name]['Terms']:
        #        if not set(terms_1).isdisjoint(terms_2):
        #           explain_dict[eval_objs[0].name]['Group'] = group_counter
        return pd.DataFrame(data=explain_dict).sort_values(by=['Terms'])

    def _get_csv_terms(self, query_id, doc_id, fields, decimal_separator, eval_objs):
        """
        Returns dict containing all the found terms and their scores.

        Parameters
        ----------
        :arg query_id: int
            query id of query that should be explained
        :arg doc_id: int
            id of document that should be explained
        :arg fields: list
            fields that should be searched
        :arg decimal_separator: string
            choose a decimal separator; by default it's a comma, but for english you might prefer a dot
        :arg eval_objs: list
            EvaluationObjs that should be compared

        Returns
        -------

        """
        term_dict = defaultdict(dict)
        for obj in eval_objs:
            explain = obj.explain_query(query_id, doc_id, fields, dumps=False)
            for field in fields:
                for function in explain[field]['details']:
                    term_dict[obj.name][field+': '+(self._extract_terms(function["function"]["description"]))] = str(
                        function["function"]["value"]).replace('.', decimal_separator)
        extra_1 = set(term_dict[eval_objs[0].name]) - set(term_dict[eval_objs[1].name])
        for key in extra_1:
            term_dict[eval_objs[1].name][key] = 0
        extra_2 = set(term_dict[eval_objs[1].name]) - set(term_dict[eval_objs[0].name])
        for key in extra_2:
            term_dict[eval_objs[0].name][key] = 0
        explain_dict = defaultdict()
        for obj in eval_objs:
            ordered_terms = collections.OrderedDict(sorted(term_dict[obj.name].items()))
            searched_terms = list(ordered_terms.keys())
            term_scores = list(ordered_terms.values())
            explain_dict[obj.name] = ['searched terms']
            explain_dict[obj.name + '2'] = ['term score']
            explain_dict[obj.name].extend(searched_terms)
            explain_dict[obj.name + '2'].extend(term_scores)
        return explain_dict

    def _extract_terms(self, string):
        """
        Extracts terms from explain_query method.

        Parameters
        ----------
        :arg string: str
            string of all the matched terms

        :Returns:
        -------
        :terms: list of str
            extracted terms

        """
        term_regx = re.compile(':[a-zA-ZäöüÄÖÜß]*\s')
        terms = re.findall(term_regx, string)
        terms = ', '.join([term.replace(':', '').strip() for term in terms])
        return terms

    def calculate_difference(self, condition='fscore', dumps=False):
        """
        Calculates the difference per query for the given condition.

        Parameters
        ----------
        :arg condition: string
            "fscore", "precision" or "recall"
        :arg dumps: True or False
            if True it returns json.dumps, if False saves to object variable

        :Returns:
        -------
        json with value differences

        """
        diff = defaultdict(dict)
        diff_name = condition + '_diffs'
        # get all condition values from the first approach
        for query, data in getattr(self.eval_obj_1, condition).items():
            if not query == 'total':
                # save for each query the difference between condition value of approach 1 and approach 2
                diff[query] = {
                    str(self.eval_obj_1.name): data[condition],
                    str(self.eval_obj_2.name): getattr(self.eval_obj_2, condition)[query][condition],
                    diff_name: abs(data[condition] - getattr(self.eval_obj_2, condition)[query][condition])}
        # sort values descending
        diff_ordered = OrderedDict(sorted(diff.items(), key=lambda i: i[1][diff_name]))
        diff_ordered['total'] = {
            str(self.eval_obj_1.name): getattr(self.eval_obj_1, condition)['total'],
            str(self.eval_obj_2.name): getattr(self.eval_obj_2, condition)['total'],
            diff_name: abs(getattr(self.eval_obj_1, condition)['total'] - getattr(self.eval_obj_2, condition)['total'])}
        if dumps:
            return json.dumps(diff_ordered, indent=4)
        else:
            setattr(self, diff_name, diff_ordered)

    def get_disjoint_sets(self, distribution, highest=False):
        """
        Returns the disjoint sets of the given distribution.

        Parameters
        ----------
        :arg distribution: str
            distribution to return; possible arguments are 'false_positives' and 'false_negatives'
        :arg highest: True or False
            if True it only returns the set with the highest count of disjoints

        :Returns:
        -------

        :ordered_results: OrderedDict
            disjoint lists for each approach in a dictionary for each query regarding the distribution

        """
        results = defaultdict(dict)
        # get query names
        for query, data in getattr(self.eval_obj_1, distribution).items():
            results[query]['question'] = data['question']
            results[query][distribution + ' ' + self.eval_obj_1.name] = []
            results[query][distribution + ' ' + self.eval_obj_2.name] = []
            # iterate over list of results in set 1 and find disjoint results
            for res_1 in data[distribution]:
                # if result is in set 1 but not in set 2 it's saved
                if not any(res_1['doc']['id'] in el['doc'].values() for el in
                           getattr(self.eval_obj_2, distribution)[query][distribution]):
                    results[query][distribution + ' ' + self.eval_obj_1.name].append(res_1)
            # iterate over list of results in set 2 and find disjoint results
            for res_2 in getattr(self.eval_obj_2, distribution)[query][distribution]:
                # if result is in set 2 but not in set 1 it's saved
                if not any(res_2['doc']['id'] in el['doc'].values() for el in
                           getattr(self.eval_obj_1, distribution)[query][distribution]):
                    results[query][distribution + ' ' + self.eval_obj_2.name].append(res_2)
            results[query]['count'] = len(results[query][distribution + ' ' + self.eval_obj_1.name]) + len(
                results[query][distribution + ' ' + self.eval_obj_2.name])
        filtered_results = {key: val for key, val in results.items() if val['count'] != 0}
        ordered_results = OrderedDict(sorted(filtered_results.items(), key=lambda i: i[1]['count']))
        if not highest:
            return ordered_results
        else:
            elements = list(ordered_results.items())
            return elements[-1]

    def get_specific_comparison(self, query_id, doc_id, fields=['text', 'title']):
        """
        Function to get position, highlights and scores for a specific query and a specific query in comparison.

        Parameters
        ----------
        :arg query_id
        :arg doc_id: int
            doc id that should be looked at
        :arg fields: list
            list of fields that should be searched on
        :Returns:
        -------
        :json.dumps(comp_dict): dict dumped as json
            filled with comparison for given query and doc id
        """
        comp_dict = defaultdict()
        attr_list = ['true_positives', 'false_positives', 'false_negatives']
        eval_objs = [self.eval_obj_1, self.eval_obj_2]
        comp_dict['Query ' + str(query_id)] = self.qrys_rels[query_id]
        comp_dict[str(self.eval_obj_1.name)] = defaultdict()
        comp_dict[str(self.eval_obj_2.name)] = defaultdict()
        for attr in attr_list:
            for obj in eval_objs:
                if 'Query_' + str(query_id) in getattr(obj, attr).keys():
                    hit_list = getattr(obj, attr)['Query_' + str(query_id)][attr]
                    for hit in hit_list:
                        if hit['doc']['id'] == doc_id:
                            try:
                                if not comp_dict[str(obj.name)]:
                                    comp_dict['Document ' + str(doc_id)] = {field: hit['doc'][field] for field in
                                                                            fields}
                                    comp_dict[str(obj.name)]['position'] = hit['position']
                                    comp_dict[str(obj.name)]['score'] = hit['score']
                                    comp_dict[str(obj.name)]['highlight'] = hit['highlight']
                                    comp_dict[str(obj.name)]['distribution'] = attr
                            except KeyError:
                                pass
        for obj in eval_objs:
            if not comp_dict[str(obj.name)]:
                logging.warning('There is no hit for query ' + str(query_id) + ' and document ' + str(doc_id) + '. This might be because of a too small size. Keep in mind that the size is 20 by default.')
        return print(json.dumps(comp_dict, indent=4))

    def visualize_distributions(self, queries=None, eval_objs=None,
                                distributions=['true_positives', 'false_positives', 'false_negatives'], download=False,
                                path_to_file='./save_vis_distributions.svg'):
        """
        Visualizes distributions in comparison for given queries and given approaches.

        Parameters
        ----------
        :arg queries: int or list or None
            if None it searches with all queries
        :arg eval_objs: list
            EvaluationObjs; if None it uses the ones already implemented in the ComparisonTool object
        :arg distributions: list
            distributions that should be printed; by default tp, fp and fn are used
        :arg download: True or False
            saves the plot as svg; by default False which leads to not saving the visualization
        :arg path_to_file: string
            path and filename the visualization should be saved to, e.g. './myfolder/save_this.svg'

        :Prints:
        -------

        visualization via matplot as plt.show()

        """
        if not eval_objs:
            eval_objs = [self.eval_obj_1, self.eval_obj_2]
        queries = eval_objs[0]._check_searched_queries(queries)
        panda_dist = self._get_distributions(queries, eval_objs, distributions)
        dist_colors = [self.pragma_colors[1], self.pragma_colors[4], self.pragma_colors[5]]
        custom_palette = sns.set_palette(sns.color_palette(dist_colors))
        sns.set_theme(context='paper', style='whitegrid', palette=custom_palette)
        plt.figure(figsize=(12, 8))
        ax = sns.countplot(x="Approach", hue="Distributions", data=panda_dist, palette=custom_palette)
        ax.set_title("true positives, false positives and false negatives")
        ax.set_xlabel("Approaches")
        ax.set_ylabel("Distributions")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if download:
            plt.gcf().subplots_adjust(bottom=0.08)
            plt.savefig(path_to_file, format="svg")
        plt.show()

    def visualize_condition(self, queries=None, eval_objs=None, conditions=['precision', 'recall', 'fscore'],
                            download=False, path_to_file='./save_vis_condition.svg'):
        """
        Visualizes conditions in comparison for given queries and given approaches.

        Parameters
        ----------
        :arg queries: int or list or None
            if None it searches with all queries
        :arg eval_objs: list
            EvaluationObjs; if None it uses the ones already implemented in the ComparisonTool object
        :arg conditions: list
            conditions that should be printed; by default precision, recall and f1-score are used
        :arg download: True or False
            saves the plot as svg; by default False which leads to not saving the visualization
        :arg path_to_file: string
            path and filename the visualization should be saved to, e.g. './myfolder/save_this.svg'

        :Prints:
        -------

        visualization via matplot as plt.show()

        """
        if conditions is None:
            conditions = ['precision', 'recall', 'fscore']
        if not eval_objs:
            eval_objs = [self.eval_obj_1, self.eval_obj_2]
        queries = eval_objs[0]._check_searched_queries(queries)
        panda_cond = self._get_conditions(queries, eval_objs, conditions)
        custom_palette = sns.set_palette(sns.color_palette(self.pragma_colors))
        sns.set_theme(context='paper', style='whitegrid', palette=custom_palette)
        g = sns.catplot(
            data=panda_cond, kind="bar",
            x="Value", y='Scores', hue="Approach",
            ci=None, alpha=.6, height=8
        )
        g.despine(left=True)
        g.set_axis_labels('Approach comparison')
        if download:
            plt.gcf().subplots_adjust(bottom=0.08)
            plt.savefig(path_to_file, format="svg")
        plt.show()

    def visualize_explanation(self, query_id, doc_id, fields=['text', 'title'], eval_objs=None, download=False,
                              path_to_file='./save_vis_explaination.svg'):
        """
        Visualize in comparison which words were better scored using approach, specific query and a specific document.

        Parameters
        ----------
        :arg queries: int or list or None
            if None it searches with all queries
        :arg doc_id: int
            id of document that should be explained
        :arg fields: list
            fields that should be searched, by default 'text' and 'title' are searched
        :arg eval_objs: list
            EvaluationObjs; if None it uses the ones already implemented in the ComparisonTool object
        :arg download: True or False
            saves the plot as svg; by default False which leads to not saving the visualization
        :arg path_to_file: string
            path and filename the visualization should be saved to, e.g. './myfolder/save_this.svg'

        :Prints:
        -------

        visualization via matplot as plt.show()

        """
        if not eval_objs:
            eval_objs = [self.eval_obj_1, self.eval_obj_2]
        panda_explain = self._get_explain_terms(query_id, doc_id, fields, eval_objs)
        custom_palette = sns.set_palette(sns.color_palette(self.pragma_colors))
        sns.set_context('paper', rc={'figure.figsize': (20, 14)})
        sns.set_theme(context='paper', style='whitegrid', palette=custom_palette)
        g = sns.barplot(x='Term Score', y='Terms', data=panda_explain, hue="Approach")
        sns.despine(left=True, bottom=True)
        if download:
            plt.gcf().subplots_adjust(bottom=0.08)
            plt.savefig(path_to_file, format="svg")
        plt.show()

    def visualize_explanation_csv(self, query_id, doc_id, path_to_save_to, fields=['text', 'title'], decimal_separator=',', eval_objs=None):
        """
        Saves explanation table to csv

        Parameters
        ----------
        :arg query_id: int
            query id of query that should be explained
        :arg doc_id: int
            id of document that should be explained
        :arg path_to_save_to: string
            path and filename the visualization should be saved to, e.g. './myfolder/save_that.csv'
        :arg fields: list
            fields that should be searched, by default 'text' and 'title' are searched
        :arg decimal_separator: string
            choose a decimal separator; by default it's a comma, but for english you might prefer a dot
        :arg eval_objs: list or None
            exactly two EvaluationObjs; if None it uses the ones from the ComparisonTool

        :Returns:
        -------
        csv file to feed it to program to create graphs, e.g. Google Sheets or Microsoft Excel

        """
        if not eval_objs:
            eval_objs = [self.eval_obj_1, self.eval_obj_2]
        panda_explain = self._get_csv_terms(query_id, doc_id, fields, decimal_separator, eval_objs)
        keys = sorted(panda_explain.keys())
        with open(path_to_save_to, "w") as outfile:
            writer = csv.writer(outfile, delimiter=";")
            writer.writerow(keys)
            writer.writerows(zip(*[panda_explain[key] for key in keys]))
