# spark_datax_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




spark_datax_tools is a Python library that implements for dataX schemas
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-datax-tools 
```


## Usage

wrapper take DataX

```sh

Nomenclature Datax
================================
table_name = "t_pmfi_lcl_suppliers_purchases"
origen = "host"
destination = "hdfs"
datax_generated_nomenclature(table_name=table_name, 
                             origen=origen, 
                             destination=destination, 
                             output=True)




List of adaptaders
================================
datax_list_adapters()




Generated Ticket Adapter
============================================================
adapter_id = "ADAPTER_HDFS_OUTSTAGING"
parameter = {"uuaa":"na8z"}
datax_generated_ticket_adapter(adapter_id=adapter_id, 
                               parameter=parameter, 
                               is_dev=True
)
                               
                               
                               
Generated Ticket Transfer
============================================================
folder="CR-PEMFIMEN-T02"	
job_name="PMFITP4012"
crq="CRQ100000"
periodicity="mensual"
hour="10AM"
weight="50MB"
origen="host"
destination="hdfs"

datax_generated_ticket_transfer(
    folder=folder,	    
    job_name=job_name,    
    crq=crq,
    periodicity=periodicity,    
    hour=hour,    
    weight=weight	,    
    table_name=table_name,    
    origen=origen,
    destination=destination,
    is_dev=True
)
                               
     
                               
Generated Schema JSON Artifactory
============================================================
path_json = "lclsupplierspurchases.output.schema"
is_schema_origen_in = True
schema_type = "host"
convert_string = False

datax_generated_schema_artifactory( 
    path_json=path_json,
    is_schema_origen_in=schema_type,
    schema_type=schema_type,
    convert_string=convert_string
)
           
   
   
   
Generated Schema Json Datum
============================================================
spark = SparkSession.builder.master("local[*]").appName("SparkAPP").getOrCreate()
path="fields_pe_datum2.csv"
table_name="t_pmfi_lcl_suppliers_purchases"
origen="host"
destination="hdfs"
storage_zone="master"

datax_generated_schema_datum(
    spark=spark,
    path=path,
    table_name=table_name,
    origen=origen,
    destination=destination,
    storage_zone=storage_zone,
    convert_string=False
)
  
```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
