#!/usr/bin/env python
"""
Publishes price / performance data

"""
import os
import copy
import pprint
import pandas as pd

from decisionengine.modules.AWS.publishers.AWS_generic_publisher import AWSGenericPublisher as publisher
import decisionengine.framework.configmanager.ConfigManager as configmanager
import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.dataspace.dataspace as dataspace
import decisionengine.modules.graphite_client as graphite

DEFAULT_GRAPHITE_CONTEXT="hepcloud_priv.aws_price_perf"
CONSUMES=['AWS_Price_Performance']

class AWSPricePerformancePublisher(publisher):
    def __init__(self, *args, **kwargs):
        super(AWSPricePerformancePublisher, self).__init__(*args, **kwargs)

    def consumes(self):
        return CONSUMES

    def graphite_context(self):
        return DEFAULT_GRAPHITE_CONTEXT

def module_config_template():
    """
    print a template for this module configuration data
    """

    d = {"AWSPricePerformancePublisher": {
        "module" :  "modules.AWS.publishers.AWS_price_performance",
        "name"   :  "AWSPricePerformancePublisher",
        },
        }
    print "Entry in channel cofiguration"
    pprint.pprint(d)
    print "where"
    print "\t name - name of the class to be instantiated by task manager"
    print "\t publish_to_graphite - publish to graphite if True"
    print "\t graphite_host - graphite host name"

def module_config_info():
    """
    print this module configuration information
    """

    print "consumes", CONSUMES
    module_config_template()



def main():
    """
    Call this a a test unit or use as CLI of this module
    """
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--configtemplate',
                        action='store_true',
                        help='prints the expected module configuration')

    parser.add_argument('--configinfo',
                        action='store_true',
                        help='prints config template along with produces and consumes info')
    args = parser.parse_args()
    if args.configtemplate:
        module_config_template()
    elif args.configinfo:
        module_config_info()
    else:
        config_manager = configmanager.ConfigManager()
        config_manager.load()
        global_config = config_manager.get_global_config()
        print "GLOBAL CONF", global_config
        ds = dataspace.DataSpace(global_config)

        data_block = datablock.DataBlock(ds,
                                         '5CC840DD-88B9-45CE-9DA2-FF531289AC66',
                                         1)

        pp_info = AWSPricePerformancePublisher({"publish_to_graphite" : False,
	                                        "graphite_host": "fermicloud399.fnal.gov",
                                                "graphite_context":"hepcloud_priv.aws_price_perf",
                                                "output_file": "%s/de_data/AWS_price_perf.csv"%(os.environ.get('HOME'),)})
        rc = pp_info.publish(data_block)

if __name__ == '__main__':
    main()
