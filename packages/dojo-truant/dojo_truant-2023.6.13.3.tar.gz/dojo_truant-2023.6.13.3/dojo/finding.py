#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Finding(dojo.DAPI):
    _endpoint = string.Template("/api/v2/findings/${id}/")
    _post_endpoint = "/api/v2/findings/"
    _search_endpoint = "/api/v2/findings/"

    _model_validation = {
        "test": {"type": (int, dojo.Test),
                 "required": True},
        "thread_id": {"type": int,
                      "required": False},
        "found_by": {"type": list,
                     "required": True},
        "url": {"type": str,
                "required": False},
        "tags": {"type": list,
                 "required": False},
        "push_to_jira": {"type": bool,
                         "required": False},
        "vulnerability_ids": {"type": list,
                              "required": False},
        "reporter": {"type": int,
                     "required": False},
        "title": {"type": str,
                  "required": True},
        "date": {"type": str,
                 "required": False,
                 "regex": "\d{4}-\d{2}-\d{2}"},
        "sla_start_date": {"type": str,
                           "required": False,
                           "regex": "\d{4}-\d{2}-\d{2}"},
        "cwe": {"type": int,
                "required": False},
        "cvssv3": {"type": str,
                   "required": False,
                   "cvss": 3},
        "cvssv3_score": {"type": float,
                         "required": False},
        "severity": {"type": str,
                     "required": True,
                     "enum": ("Critical", "High", "Medium", "Low", "Informtional")},
        "description": {"type": str,
                        "required": True},
        "mitigation": {"type": str,
                       "required": False},
        "impact": {"type": str,
                   "required": False},
        "steps_to_reproduce": {"type": str,
                               "required": False},
        "severity_justification": {"type": str,
                                   "required": False},
        "references": {"type": str,
                       "required": False},
        "active": {"type": bool,
                   "required": True},
        "verified": {"type": bool,
                     "required": True},
        "false_p": {"type": bool,
                    "required": False},
        "duplicate": {"type": bool,
                      "required": False},
        "out_of_scope": {"type": bool,
                         "required": False},
        "risk_accepted": {"type": bool,
                          "required": False},
        "under_review": {"type": bool,
                         "required": False},
        "under_defect_review": {"type": bool,
                                "required": False},
        "is_mitigated": {"type": bool,
                         "required": False},
        "numerical_severity": {"type": str,
                               "required": True},
        "line": {"type": int,
                 "required": False},
        "file_path": {"type": str,
                      "required": False},
        "component_name": {"type": str,
                           "required": False},
        "component_version": {"type": str,
                              "required": False},
        "static_finding": {"type": bool,
                           "required": False},
        "dynamic_finding": {"type": bool,
                            "required": False},
        "unique_id_from_tool": {"type": str,
                                "required": False},
        "vuln_id_from_tool": {"type": str,
                              "required": False},
        "sast_source_object": {"type": str,
                               "required": False},
        "sast_sink_object": {"type": str,
                             "required": False},
        "sast_source_line": {"type": str,
                             "required": False},
        "sast_source_file_path": {"type": str,
                                  "required": False},
        "nb_occurences": {"type": int,
                          "required": False},
        "publish_date": {"type": str,
                         "required": False,
                         "regex": "\d{4}-\d{2}-\d{2}"},
        "service": {"type": str,
                    "required": False},
        "planned_remediation_date": {"type": str,
                                     "required": False,
                                     "regex": "\d{4}-\d{2}-\d{2}"},

        "review_requested_by": {"type": int,
                                "required": False},

        "defect_review_requested_by": {"type": int,
                                       "required": False},

        "sonarcube_issue": {"type": int,
                            "required": False},

        "reviewers": {"type": list,
                      "required": False},

    }

    _obj_iterate = ".results[]"

    _type = "finding"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Finding")

    #def add_note(self, note_text):

        '''
        Adds a Note to a Finding
        '''

    #def add_tag(self, tag):

        '''
        Adds a Tag to a Finding
        '''

    def add_meta(self, name=None, value=None, overwrite=False):

        '''
        Adds a Metadata Object to this Finding
        '''

        existing_metadata_endpoint = "api/v2/findings/{}/metadata/".format(self.id)

        current_metadata_json = self.api_call(endpoint=existing_metadata_endpoint,
                                              method="GET",
                                              token=True,
                                              return_json=True)

        current_metadata = {x["name"]: x["value"] for x in current_metadata_json}

        if str(name) not in current_metadata.keys() or overwrite is True:
            # Place New metadata

            new_meta = {"name": str(name),
                        "value": str(value)}

            new_metadata_json = self.api_call(endpoint=existing_metadata_endpoint,
                                              method="POST",
                                              token=True,
                                              json=new_meta,
                                              return_json=True)

        else:
            self.logger.debug("Not Overwriting Current Metadata")
