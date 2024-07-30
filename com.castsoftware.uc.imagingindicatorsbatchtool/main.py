# import socket
import traceback
import time
import os, sys
import csv
from requests.auth import HTTPBasicAuth
import requests
import json
# sys.path.append(r"C:\Users\SHP\eclipse-workspace\com.castsoftware.uc.imagingindicators.1.0.1\com.castsoftware.uc.imagingindicatorsbatchtool")
#from psycopg2 import connect
import psycopg2

class Report():
     
    def __init__(self, application_name, local_DB_name, local_DB_host, local_DB_port, local_DB_user, local_DB_password, console_url, console_username, console_password, central_DB_name, central_DB_host, central_DB_port, central_DB_user, central_DB_password):
        self.application_name = application_name
        self.local_DB_name = local_DB_name
        self.local_DB_host = local_DB_host
        self.local_DB_port = int(local_DB_port)
        self.local_DB_user = local_DB_user
        self.local_DB_password = local_DB_password

        self.console_url = console_url
        self.console_username = console_username
        self.console_password = console_password

        self.central_DB_name = central_DB_name
        self.central_DB_host = central_DB_host
        self.central_DB_port = int(central_DB_port)
        self.central_DB_user = central_DB_user
        self.central_DB_password = central_DB_password
        
        self.itrtn_no = 1
        self.app_name = 'NULL'
        self.start_date_time = 'NULL'
        self.end_date_time = 'NULL'
        self.no_of_scans_to_make_anlys_cmplnt_with_IMA = 0
        self.app_size_in_KLOC = 0.0
        self.artfct_cvrge_ratio = 0
        self.no_of_complex_trans = 0
        self.data_entities_by_trans = 0
        self.ratio_of_complete_trans_LOC = 0.0
        self.ratio_of_non_empty_trans = 0
        self.class_coverage_ratio = 0.0
        #self.prog_in_trans = 0.0
        self.no_of_links = 0
        self.ratio_of_msg_que = 'NULL'
        self.ratio_of_soap_java_ope = 'NULL'
        self.ratio_of_rest_call = 'NULL'
        self.ratio_of_ope_call = 'NULL'
        self.no_of_unrev_dyn_lick = 0
        self.ratio_of_spring_mvc = 'NULL'
        self.ratio_of_typescript_angular_node_calls = 'NULL'
        self.AEFP_AETP_ratio = 0
        self.logs_info_missing_file_dll_jars = 'NULL'
        self.TFP_DFP_ratio = 0
        self.no_of_valid_entry_points = 0
        self.no_of_valid_endpoints = 0
        self.no_of_exclusion = 0
        self.unanalyzed_code = 0
        self.missing_tables = 0
        self.no_of_tickets_to_make_ana_compliant_with_IMG = 0
        self.technology = 'NULL'
        self.extn_installed = 'NULL'
        self.use_case = 0
        self.tech_code_review = 0

    def create_IMG_INDICATORS_table(self, con, kb):
        try:
            print("creating table IMG_INDICATORS.......")
            cursor_obj = con.cursor()
            cursor_obj.execute("SET search_path TO {}".format(kb))
            cursor_obj.execute("""CREATE TABLE IF NOT EXISTS IMG_INDICATORS( itrtn_no INT, app_name VARCHAR(100), start_date_time VARCHAR(100), end_date_time VARCHAR(100),
            no_of_scans_to_make_anlys_cmplnt_with_IMA INT, app_size_in_KLOC FLOAT, artfct_cvrge_ratio VARCHAR(1000), no_of_complex_trans  INT, 
            data_entities_by_trans INT, ratio_of_complete_trans_LOC FLOAT, ratio_of_non_empty_trans INT, class_coverage_ratio FLOAT, 
             no_of_links INT, ratio_of_msg_que VARCHAR(50), ratio_of_soap_java_ope VARCHAR(50), ratio_of_rest_call VARCHAR(50),
            ratio_of_ope_call VARCHAR(50), no_of_unrev_dyn_lick INT, ratio_of_spring_mvc VARCHAR(50), ratio_of_typescript_angular_node_calls VARCHAR(50), 
            AEFP_AETP_ratio INT, logs_info_missing_file_dll_jars VARCHAR(1000), TFP_DFP_ratio FLOAT, no_of_valid_entry_points INT, 
            no_of_valid_endpoints INT, no_of_exclusion INT, unanalyzed_code INT, missing_tables INT, no_of_tickets_to_make_ana_compliant_with_IMG INT, 
            technology VARCHAR(1000), extn_installed VARCHAR(10000), use_case INT, tech_code_review INT);""")

            con.commit()

        except Exception as e:
            print("Some exception has occurred while creating table -> "+str(e))

        else:    
            print("created IMG_INDICATORS table.")

    def after_snapshot(self, con, application_name, kb, mngt, central):

        print('kb -> '+str(kb))
        print('mngt -> '+str(mngt))
        print('central -> '+str(central))

        self.start_date_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        print('start_date_time -> '+str(self.start_date_time))
        
        try:
            cursor_1 = con.cursor()
            cursor_1.execute("SET search_path TO {}".format(kb))
            cursor_1.execute("""SELECT itrtn_no FROM img_indicators ORDER BY itrtn_no DESC LIMIT 1;""")
            # print(cursor_1.fetchall())
            # print(type(cursor_1.fetchall()))
            self.itrtn_no = int(cursor_1.fetchall()[0][0]) + 1
            if self.itrtn_no is None:
                self.itrtn_no = 1
                
        except Exception as e:
            self.itrtn_no = 1

        print('itrtn_no -> '+str(self.itrtn_no))
        
        print('app_name -> '+str(self.application_name))
        
        cursor_2 = con.cursor()
        cursor_2.execute("SET search_path TO {}".format(mngt))
        cursor_2.execute("""select count(*) from tasklog_history where lower(log_context) like lower('%Execute_Analysis%MainTask_SummaryLog%')""")
        # print(cursor_2.fetchall()[0])
        # res = cursor_2.fetchall()
        # print(res)
        # print(type(cursor_2.fetchall()))
        self.no_of_scans_to_make_anlys_cmplnt_with_IMA = cursor_2.fetchall()[0][0]
        if self.no_of_scans_to_make_anlys_cmplnt_with_IMA is None:
            self.no_of_scans_to_make_anlys_cmplnt_with_IMA = 0
        print('no_of_scans_to_make_anlys_cmplnt_with_IMA -> '+str(self.no_of_scans_to_make_anlys_cmplnt_with_IMA))    

        cursor_3 = con.cursor()
        cursor_3.execute("SET search_path TO {}".format(central))
        cursor_3.execute("""select dmr.metric_num_value from dss_metric_results dmr, dss_metric_types dmt, dss_objects o 
        where dmr.metric_id = dmt.metric_id and dmr.object_id = o.object_id and o.object_type_id = -102 and snapshot_id = (select max(snapshot_id) from dss_snapshots) and 
        (dmr.metric_value_index = 1 and dmr.metric_id in (10151))""")
        self.app_size_in_KLOC = cursor_3.fetchall()[0][0]
        if self.app_size_in_KLOC is None or self.app_size_in_KLOC is '':
            self.app_size_in_KLOC = 0.0
        #

        cursor_4 = con.cursor()
        cursor_4.execute("SET search_path TO {}".format(kb))
        cursor_4.execute("""select 
        cast((covered_count*100/ case when total_count = 0 then 1 else total_count end)as text) ||'%' as percentage_ratio from
        ( select count(distinct cdt.object_id) as total_count from cdt_objects cdt, ctt_object_applications ctt where 
        cdt.object_id = ctt.object_id and ctt.properties <> 1 and cdt.object_type_str in ('Progress Program', 'Cobol Program', 'C++ Class'
        , 'VB.NET Class', 'ColdFusion Fuse Action', 'VB MDI Form', 'SHELL Program', 'ColdFusion Template', 'C/C++ File', 'C# Class'
        , 'Java Class', 'VB Module', 'Session')) total, (select count(distinct cdt.object_id) as covered_count from cdt_objects cdt,
        ctt_object_applications ctt where cdt.object_id = ctt.object_id and ctt.properties <> 1 and ctt.object_id in
        (select object_id from cdt_objects where object_id in ( select distinct child_id from dss_transactiondetails) union 
        select parent_id from ctt_object_parents where object_id in (select distinct child_id from dss_transactiondetails) union
        select called_id from ctv_links where caller_id in (select distinct child_id from dss_transactiondetails) union
        select called_id from ctv_links where caller_id in (select distinct called_id from ctv_links where caller_id in
        (select distinct child_id from dss_transactiondetails)) union select parent_id from ctt_object_parents where object_id in
        (select distinct called_id from ctv_links where caller_id in (select distinct child_id from dss_transactiondetails))union 
        select parent_id from ctt_object_parents where object_id in (select distinct called_id from ctv_links where caller_id in
        (select distinct called_id from ctv_links where caller_id in (select distinct child_id from dss_transactiondetails))) union
        select object_id from ctt_object_parents where parent_id in (select distinct parent_id from ctt_object_parents where object_id in
        ( select distinct child_id from dss_transactiondetails)) union select object_id from ctt_object_parents where parent_id in
        ( select distinct parent_id from ctt_object_parents where object_id in ( select distinct called_id from ctv_links where caller_id in
        ( select distinct child_id from dss_transactiondetails))) union select object_id from ctt_object_parents where parent_id in
        (select distinct parent_id from ctt_object_parents where object_id in ( select distinct called_id from ctv_links where caller_id in
        (select distinct called_id from ctv_links where caller_id in ( select distinct child_id from dss_transactiondetails)))))
        and cdt.object_type_str in ('Progress Program','Cobol Program','C++ Class','VB.NET Class','ColdFusion Fuse Action'
        ,'VB MDI Form','SHELL Program','ColdFusion Template','C/C++ File','C# Class','Java Class','VB Module','Session')) covered""")
        self.artfct_cvrge_ratio = cursor_4.fetchall()[0][0]
        if self.artfct_cvrge_ratio is None:
            self.artfct_cvrge_ratio = 0
        print('artfct_cvrge_ratio -> '+str(self.artfct_cvrge_ratio) )
        
        cursor_5 = con.cursor()
        cursor_5.execute("SET search_path TO {}".format(kb))
        #cursor_5.execute("""select count(1) from dss_transactiondetails""")
        cursor_5.execute("""SELECT COUNT(*) FROM (select count(child_id) from dss_transactiondetails group by object_id having count(child_id) >= 5000) as count""")
        self.no_of_complex_trans = cursor_5.fetchall()[0][0]
        if self.no_of_complex_trans is None:
            self.no_of_complex_trans = 0
        print('no_of_complex_trans -> '+str(self.no_of_complex_trans) )
            
        cursor_6 = con.cursor()
        cursor_6.execute("SET search_path TO {}".format(kb))
        cursor_6.execute("""select count(object_id) from cdt_objects where lower(object_type_str) like '%table%' and object_id in 
        (select child_id from dss_transactiondetails);""")
        self.data_entities_by_trans = cursor_6.fetchall()[0][0]
        if self.data_entities_by_trans is None:
            self.data_entities_by_trans = 0
        print('data_entities_by_trans -> '+str(self.data_entities_by_trans))
        
        cursor_7 = con.cursor()
        cursor_7.execute("SET search_path TO {}".format(kb))
        cursor_7.execute("""select round((afp.fp:: float/codelines.LOC :: float), 2)
        from (select sum(oi.infval) as LOC FROM   objinf oi, keys k, cdt_objects cdt, csv_file_objects cfo
        WHERE  oi.idobj IN (SELECT ( object_id ) FROM   ctt_object_applications
        WHERE  --application_id = <application_id >
                          -- AND
        properties = 0) AND inftyp = 1 AND infsubtyp = 0 AND k.idkey = oi.idobj AND k.objtyp IN (SELECT DISTINCT t.idtyp
        FROM   typ t, typcat tc WHERE  t.idtyp = tc.idtyp AND tc.idcatparent IN 
        (SELECT cat.idcat FROM   cat WHERE catnam LIKE 'APM Sources'))
        AND  cdt.object_id =oi.idobj and cfo.object_id = cdt.object_id and upper(cfo.file_path) not like '%LISA%'
        and upper(cfo.file_path) not like '%LTSA%') as CodeLines, (select  (tfp.tf + dfp.df) fp
        from (select sum(tf_ex) as tf from dss_transaction where cal_flags = 0) as tfp,
        (select sum(ilf_ex) as df from dss_datafunction where cal_flags = 0) as dfp) as afp;""")
        self.ratio_of_complete_trans_LOC = cursor_7.fetchall()[0][0]
        if self.ratio_of_complete_trans_LOC is None:
            self.ratio_of_complete_trans_LOC = 0
        print('ratio_of_complete_trans_LOC -> '+str(self.ratio_of_complete_trans_LOC))
            
        cursor_8 = con.cursor()
        cursor_8.execute("SET search_path TO {}".format(kb))
        cursor_8.execute("""select cast( ((tb_empty_tr.tr_count  * 100)/ nullif(tb_all_tr.tr_count,0)) as text) as percentage_ratio
        from (select count(cob.object_name) as tr_count from dss_transaction dtr, cdt_objects cob
        where dtr.form_id = cob.object_id and dtr.cal_mergeroot_id = 0  and dtr.cal_flags not in (  8, 10, 126, 128,136, 138, 256, 258 ) ) tb_all_tr,
        (select count(cob.object_name) as tr_count from dss_transaction dtr, cdt_objects cob where dtr.form_id = cob.object_id and dtr.cal_mergeroot_id = 0  
        and dtr.cal_flags not in (  8, 10, 126, 128,136, 138, 256, 258 )  and DTR.tf_ex=0  ) tb_empty_tr;""")
        self.ratio_of_non_empty_trans = cursor_8.fetchall()[0][0]
        if self.ratio_of_non_empty_trans is None:
            self.ratio_of_non_empty_trans = 0
        self.ratio_of_non_empty_trans = 100 - int(self.ratio_of_non_empty_trans)
        print('ratio_of_non_empty_trans -> '+str(self.ratio_of_non_empty_trans))
            
        cursor_9 = con.cursor()
        cursor_9.execute("SET search_path TO {}".format(central))
        cursor_9.execute("""select  cast(fp_to_pgmclass_ratio as text) as percentage_ratio from(
        select pgm_classes.pgm_count Programs_Class, fp_count.fp FP, round(CASE WHEN pgm_classes.pgm_count = 0::numeric THEN 0::numeric
        ELSE fp_count.fp / pgm_classes.pgm_count END, 2) AS fp_to_pgmclass_ratio from 
        (select sum(metric_num_value) as pgm_count from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10155, 10156)) as pgm_classes,
        (select sum(metric_num_value) as fp from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 and t1.snapshot_id = 
        (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10203, 10204)) as fp_count ) as dataTable """)
        self.class_coverage_ratio = cursor_9.fetchall()[0][0]
        if self.class_coverage_ratio is None:
            self.class_coverage_ratio = 0.0
        print('class_coverage_ratio -> '+str(self.class_coverage_ratio))       
        

        cursor_10 = con.cursor()
        cursor_10.execute("SET search_path TO {}".format(central))
        cursor_10.execute("""select cast(fp_to_pgmclass_ratio as text) as percentage_ratio from(
        select pgm_classes.pgm_count Programs_Class, fp_count.fp FP, 
        round( CASE WHEN pgm_classes.pgm_count = 0::numeric THEN 0::numeric 
        ELSE fp_count.fp / pgm_classes.pgm_count END, 2) AS fp_to_pgmclass_ratio  from 
        (select sum(metric_num_value) as pgm_count from dss_metric_results t1, dss_metric_types t2, 
        dss_objects t3 where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10155, 10156)) as pgm_classes,
        (select sum(metric_num_value) as fp from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots)
        and t1.metric_id in ( 10203, 10204)) as fp_count ) as dataTable """)
        self.prog_in_trans = cursor_10.fetchall()[0][0]
        if self.prog_in_trans is None:
            self.prog_in_trans = 0
        print('prog_in_trans -> '+str(self.prog_in_trans))
        

        cursor_11 = con.cursor()
        cursor_11.execute("SET search_path TO {}".format(kb))
        cursor_11.execute("""select count(1) from CTV_links;""")
        self.no_of_links = cursor_11.fetchall()[0][0]
        if self.no_of_links is None:
            self.no_of_links = 0
        print('no_of_links -> '+str(self.no_of_links))
            
        cursor_12 = con.cursor()
        cursor_12.execute("SET search_path TO {}".format(kb))
        cursor_12.execute("""select CONCAT(( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('IBM MQ Java Queue Publisher', 'IBM MQ Java Queue Receiver', 'IBM MQ Java Topic Publisher', 'IBM MQ Java Topic Receiver', 'IBM MQ Java Unknown Queue Publisher', 'IBM MQ Java Unknown Queue Receiver', 'IBM MQ Java Unknown Topic Publisher', 'IBM MQ Java Unknown Topic Receiver', 'Java AWS Simple Queue Service Publisher', 'Java AWS Simple Queue Service Receiver', 'Java AWS Simple Queue Service Unknown Publisher', 'Java AWS Simple Queue Service Unknown Receiver', 'JMS Java Queue Publisher', 'JMS Java Queue Receiver', 'JMS Java Topic Publisher', 'JMS Java Topic Receiver', 'JMS Java Unknown Queue Publisher', 'JMS Java Unknown Queue Receiver', 'JMS Java Unknown Topic Publisher', 'JMS Java Unknown Topic Receiver', 'RabbitMQ Java Queue Publisher', 'RabbitMQ Java Queue Receiver', 'RabbitMQ Unknown Java Queue Publisher', 'RabbitMQ Unknown Java Queue Receiver')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1 where co1.object_type_str in ('IBM MQ Java Queue Publisher', 'IBM MQ Java Queue Receiver', 'IBM MQ Java Topic Publisher', 'IBM MQ Java Topic Receiver', 'IBM MQ Java Unknown Queue Publisher', 'IBM MQ Java Unknown Queue Receiver', 'IBM MQ Java Unknown Topic Publisher', 'IBM MQ Java Unknown Topic Receiver', 'Java AWS Simple Queue Service Publisher', 'Java AWS Simple Queue Service Receiver', 'Java AWS Simple Queue Service Unknown Publisher', 'Java AWS Simple Queue Service Unknown Receiver', 'JMS Java Queue Publisher', 'JMS Java Queue Receiver', 'JMS Java Topic Publisher', 'JMS Java Topic Receiver', 'JMS Java Unknown Queue Publisher', 'JMS Java Unknown Queue Receiver', 'JMS Java Unknown Topic Publisher', 'JMS Java Unknown Topic Receiver', 'RabbitMQ Java Queue Publisher', 'RabbitMQ Java Queue Receiver', 'RabbitMQ Unknown Java Queue Publisher', 'RabbitMQ Unknown Java Queue Receiver')))""")
        self.ratio_of_msg_que = cursor_12.fetchall()[0][0]
        if self.ratio_of_msg_que is None:
            self.ratio_of_msg_que = 'null'
        print('ratio_of_msg_que -> '+str(self.ratio_of_msg_que))
            
        cursor_13 = con.cursor()
        cursor_13.execute("SET search_path TO {}".format(kb))
        cursor_13.execute("""select CONCAT((select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('SOAP Client end point', 'SOAP Java Client', 'SOAP Java Client Operation', 'SOAP Java Operation', 'SOAP Java Port Type', 'SOAP Java Web Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1 where co1.object_type_str in ('SOAP Client end point', 'SOAP Java Client', 'SOAP Java Client Operation', 'SOAP Java Operation', 'SOAP Java Port Type', 'SOAP Java Web Service')))""")
        self.ratio_of_soap_java_ope = cursor_13.fetchall()[0][0]
        if self.ratio_of_soap_java_ope is None:
            self.ratio_of_soap_java_ope = 'null'
        print('ratio_of_soap_java_ope -> '+str(self.ratio_of_soap_java_ope))
            
        cursor_14 = con.cursor()
        cursor_14.execute("SET search_path TO {}".format(kb))
        cursor_14.execute("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Patch Resource Service', 'Delete Resource Service', 'Get Resource Service', 'Post Resource Service', 'Put Resource Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Patch Resource Service', 'Delete Resource Service', 'Get Resource Service', 'Post Resource Service', 'Put Resource Service')))""")
        self.ratio_of_rest_call = cursor_14.fetchall()[0][0]
        if self.ratio_of_rest_call is None:
            self.ratio_of_rest_call = 'null'
        print('ratio_of_rest_call -> '+str(self.ratio_of_rest_call))
              
        cursor_15 = con.cursor()
        cursor_15.execute("SET search_path TO {}".format(kb))
        cursor_15.execute("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('JAX-RS Delete Operation Service', 'JAX-RS Get Operation Service', 'JAX-RS Get Resource Service', 'JAX-RS Post Operation Service', 'JAX-RS Put Operation Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('JAX-RS Delete Operation Service', 'JAX-RS Get Operation Service', 'JAX-RS Get Resource Service', 'JAX-RS Post Operation Service', 'JAX-RS Put Operation Service')))""")
        self.ratio_of_ope_call = cursor_15.fetchall()[0][0]
        if self.ratio_of_ope_call is None:
            self.ratio_of_ope_call = 'null'
        print('ratio_of_ope_call -> '+str(self.ratio_of_ope_call))
        
        cursor_16 = con.cursor()
        cursor_16.execute("SET search_path TO {}".format(kb))
        cursor_16.execute("""Select count(prop) from acc where prop = 1;""")
        self.no_of_unrev_dyn_lick = cursor_16.fetchall()[0][0]
        if self.no_of_unrev_dyn_lick is None:
            self.no_of_unrev_dyn_lick = 0
        print('no_of_unrev_dyn_lick -> '+str(self.no_of_unrev_dyn_lick))
        
        cursor_17 = con.cursor()
        cursor_17.execute("SET search_path TO {}".format(kb))
        cursor_17.execute("""select CONCAT((select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Spring MVC Any Operation', 'Spring MVC Delete Operation', 'Spring MVC Get Operation', 'Spring MVC Post Operation', 'Spring MVC Put Operation', 'Spring MVC Service', 'Thymeleaf DELETE resource service', 'Thymeleaf GET resource service', 'Thymeleaf POST resource service', 'Thymeleaf PUT resource service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Spring MVC Any Operation', 'Spring MVC Delete Operation', 'Spring MVC Get Operation', 'Spring MVC Post Operation', 'Spring MVC Put Operation', 'Spring MVC Service', 'Thymeleaf DELETE resource service', 'Thymeleaf GET resource service', 'Thymeleaf POST resource service', 'Thymeleaf PUT resource service')))""")
        self.ratio_of_spring_mvc = cursor_17.fetchall()[0][0]
        if self.ratio_of_spring_mvc is None:
            self.ratio_of_spring_mvc = 'null'
        print('ratio_of_spring_mvc -> '+str(self.ratio_of_spring_mvc))
        
        cursor_18 = con.cursor()
        cursor_18.execute("SET search_path TO {}".format(kb))
        cursor_18.execute("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Angular GET http service', 'TypeScript GET http service', 'Angular POST http service', 'TypeScript POST http service', 'Angular PUT http service', 'TypeScript PUT http service', 'Angular DELETE http service', 'TypeScript DELETE http service', 'Node.js Delete Operation Service', 'Node.js Get Operation Service', 'Node.js Post Operation Service', 'Node.js Put Operation Service', 'Node.js MongoDB connection', 'Node.js MongoDB collection', 'Node.js AWS SQS Publisher', 'Node.js AWS SQS', 'Node.js AWS SQS Unknown Publisher', 'Node.js AWS SQS Unknown', 'Node.js AWS SNS Publisher', 'Node.js AWS SNS Subscriber', 'Node.js AWS SNS Unknown Publisher', 'Node.js AWS SNS Unknown Subscriber', 'Node.js AWS Lambda Post Operation Service', 'Node.js AWS Lambda Put Operation Service', 'Node.js AWS Lambda Delete Operation Service', 'Node.js AWS Lambda Any Operation Service', 'Node.js Call to Lambda', 'Node.js Call to unknown Lambda')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Angular GET http service', 'TypeScript GET http service', 'Angular POST http service', 'TypeScript POST http service', 'Angular PUT http service', 'TypeScript PUT http service', 'Angular DELETE http service', 'TypeScript DELETE http service', 'Node.js Delete Operation Service', 'Node.js Get Operation Service', 'Node.js Post Operation Service', 'Node.js Put Operation Service', 'Node.js MongoDB connection', 'Node.js MongoDB collection', 'Node.js AWS SQS Publisher', 'Node.js AWS SQS', 'Node.js AWS SQS Unknown Publisher', 'Node.js AWS SQS Unknown', 'Node.js AWS SNS Publisher', 'Node.js AWS SNS Subscriber', 'Node.js AWS SNS Unknown Publisher', 'Node.js AWS SNS Unknown Subscriber', 'Node.js AWS Lambda Post Operation Service', 'Node.js AWS Lambda Put Operation Service', 'Node.js AWS Lambda Delete Operation Service', 'Node.js AWS Lambda Any Operation Service', 'Node.js Call to Lambda', 'Node.js Call to unknown Lambda')))""")
        self.ratio_of_typescript_angular_node_calls = cursor_18.fetchall()[0][0]
        if self.ratio_of_typescript_angular_node_calls is None:
            self.ratio_of_typescript_angular_node_calls = 'null'
        print('ratio_of_typescript_angular_node_calls -> '+str(self.ratio_of_typescript_angular_node_calls))
        
        cursor_19 = con.cursor()
        cursor_19.execute("SET search_path TO {}".format(central))
        cursor_19.execute("""SELECT  
        CASE 
            WHEN c4.metric_num_value <> 0 THEN 
            ROUND(((c1.metric_num_value) / NULLIF((c1.metric_num_value + c2.metric_num_value), 0)) * 100, 2)
            ELSE 0 
        END AS varPercent  
        FROM   
        dss_metric_results c1, 
        dss_metric_results c2, 
        dss_metric_results c3, 
        dss_metric_results c4  
        WHERE 
        c1.metric_id = 10430 
        AND c2.metric_id = 10440  
        AND c3.metric_id = 10430 
        AND c4.metric_id = 10440  
        AND c1.object_id IN (SELECT object_id FROM dss_objects WHERE object_type_id = -102)   
        AND c2.object_id IN (SELECT object_id FROM dss_objects WHERE object_type_id = -102)  
        AND c1.snapshot_id = (SELECT MAX(snapshot_id) FROM dss_snapshots)  
        AND c2.snapshot_id = (SELECT MAX(snapshot_id) FROM dss_snapshots)  
        AND c3.snapshot_id = (SELECT snapshot_id FROM (SELECT snapshot_id FROM dss_snapshots ORDER BY snapshot_id DESC LIMIT 2) AS snapid ORDER BY snapshot_id LIMIT 1) 
        AND c3.object_id IN (SELECT object_id FROM dss_objects WHERE object_type_id = -102)   
        AND c4.object_id IN (SELECT object_id FROM dss_objects WHERE object_type_id = -102) 
        AND c4.snapshot_id = (SELECT snapshot_id FROM (SELECT snapshot_id FROM dss_snapshots ORDER BY snapshot_id DESC LIMIT 2) AS snapid ORDER BY snapshot_id LIMIT 1);""")
        self.AEFP_AETP_ratio = cursor_19.fetchall()[0][0]
        if self.AEFP_AETP_ratio is None:
            self.AEFP_AETP_ratio = 0
        print('AEFP_AETP_ratio -> '+str(self.AEFP_AETP_ratio))

        cursor_20 = con.cursor()
        cursor_20.execute("SET search_path TO {}".format(kb))
        cursor_20.execute("""select cast((TFP + .0001)/(DFP +.0001) as text) as percentage_ratio
        from (select sum(DTR.tf_ex) as TFP from dss_transaction dtr, cdt_objects cob where dtr.form_id = cob.object_id
        and dtr.cal_mergeroot_id = 0 and dtr.cal_flags not in ( 8, 10, 126, 128,136, 138, 256, 258 ) ) as TFP,
        ( select sum(dtf.ilf_ex) as DFP from dss_datafunction dtf, cdt_objects cob where dtf.maintable_id = cob.object_id and dtf.cal_flags in (0,2)) as DFP;""")
        self.TFP_DFP_ratio = cursor_20.fetchall()[0][0]
        if self.TFP_DFP_ratio is None:
            self.TFP_DFP_ratio = 0.0
        print('TFP_DFP_ratio -> '+str(self.TFP_DFP_ratio))
           
        cursor_21 = con.cursor()
        cursor_21.execute("SET search_path TO {}".format(kb))
        cursor_21.execute("""select count(distinct(cdt.object_type_str)) from cdt_objects cdt, dss_transaction dt
        where dt.cal_flags = 0 and dt.form_id = cdt.object_id""")
        self.no_of_valid_entry_points = cursor_21.fetchall()[0][0]
        if self.no_of_valid_entry_points is None:
            self.no_of_valid_entry_points = 0
        print('no_of_valid_entry_points -> '+str(self.no_of_valid_entry_points))
         
        cursor_22 = con.cursor()
        cursor_22.execute("SET search_path TO {}".format(kb))
        cursor_22.execute("""select count(distinct(cdt.object_type_str))
        from cdt_objects cdt, fp_dataendpoints de where cdt.object_id = de.object_id""")
        self.no_of_valid_endpoints = cursor_22.fetchall()[0][0]
        if self.no_of_valid_endpoints is None:
            self.no_of_valid_endpoints = 0
        print('no_of_valid_endpoints -> '+str(self.no_of_valid_endpoints))
        
        cursor_23 = con.cursor()
        cursor_23.execute("SET search_path TO {}".format(kb))
        cursor_23.execute("""select  count(distinct(cdt.object_type_str))
        from cdt_objects cdt, fp_result_excludedobjects fre where cdt.object_id = fre.object_id""")
        self.no_of_exclusion = cursor_23.fetchall()[0][0]
        if self.no_of_exclusion is None:
            self.no_of_exclusion = 0
        print('no_of_exclusion -> '+str(self.no_of_exclusion))
        
        cursor_24 = con.cursor()
        cursor_24.execute("SET search_path TO {}".format(kb))
        cursor_24.execute("""SELECT STRING_AGG(distinct(object_language_name), ', ') FROM cdt_objects where object_language_name not like '%N/A%'""")
        self.technology = cursor_24.fetchall()[0][0]
        if self.technology is None:
            self.technology = 'null'
        print('technology -> '+str(self.technology))
            
        cursor_25 = con.cursor()
        cursor_25.execute("SET search_path TO {}".format(kb))
        #cursor_25.execute("""select STRING_AGG(distinct(package_name), ', ') from sys_package_version where package_name like '%com%'""")
        cursor_25.execute("""select STRING_AGG(distinct package_name ||'--'|| version,', ') as extensions from sys_package_version where package_name like '/com%'""")
        self.extn_installed = cursor_25.fetchall()[0][0]
        if self.extn_installed is None:
            self.extn_installed = 'null'
        print('extn_installed -> '+str(self.extn_installed))
            
        cursor_26 = con.cursor()
        cursor_26.execute("SET search_path TO {}".format(central))
        cursor_26.execute("""SELECT COUNT(1) AS "ARTIFACTS_NOT_CONTRIBUTING_TO_FP"
        FROM AEP_TECHNICAL_ARTIFACTS_VW A 
		where A.snapshot_id = (select max (snapshot_id) from dss_snapshots)
		and A.status != 'DELETED'""")
        self.tech_code_review = cursor_26.fetchall()[0][0]
        if self.tech_code_review is None:
            self.tech_code_review = 0
        print('tech_code_review -> '+str(self.tech_code_review))
        

        self.end_date_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        print('end_date_time -> '+str(self.end_date_time)) 
            
            
        print('Inserting data into IMG_INDICATORS CSV File.....')
        print('IMG_INDICATORS CSV File Present at the location -> '+os.getcwd()+"\IMG_INDICATORS_Report_for_{}.csv".format(self.application_name))
        try:
            # generate a path in LISA my_report<timestamp>.xlxs 
            report_path = os.path.join(os.getcwd(), "IMG_INDICATORS_Report_for_{}.csv".format(self.application_name))
            
            if not os.path.exists(report_path):
                print("creating IMG_INDICATORS_Report_for_{}.csv ......".format(self.application_name))
                
                with open(report_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                     
                    writer.writerow(["itrtn_no", "app_name", "start_date_time", "end_date_time", "no_of_scans_to_make_anlys_cmplnt_with_IMA", "app_size_in_KLOC", "artfct_cvrge_ratio", "no_of_complex_trans","data_entities_by_trans","ratio_of_complete_trans_LOC", "ratio_of_non_empty_trans", "class_coverage_ratio",  "no_of_links", "ratio_of_msg_que", "ratio_of_soap_java_ope", "ratio_of_rest_call", "ratio_of_ope_call", "no_of_unrev_dyn_lick", "ratio_of_spring_mvc", "ratio_of_typescript_angular_node_calls", "AEFP_AETP_ratio", "logs_info_missing_file_dll_jars", "TFP_DFP_ratio", "no_of_valid_entry_points", "no_of_valid_endpoints", "no_of_exclusion", "unanalyzed_code", "missing_tables", "no_of_tickets_to_make_ana_compliant_with_IMG", "technology", "extn_installed", "use_case", "tech_code_review"])
                    writer.writerow([self.itrtn_no, self.application_name, self.start_date_time, self.end_date_time, self.no_of_scans_to_make_anlys_cmplnt_with_IMA, self.app_size_in_KLOC, self.artfct_cvrge_ratio, self.no_of_complex_trans,self.data_entities_by_trans,self.ratio_of_complete_trans_LOC, self.ratio_of_non_empty_trans, self.class_coverage_ratio,  self.no_of_links, self.ratio_of_msg_que, self.ratio_of_soap_java_ope, self.ratio_of_rest_call, self.ratio_of_ope_call, self.no_of_unrev_dyn_lick, self.ratio_of_spring_mvc, self.ratio_of_typescript_angular_node_calls, self.AEFP_AETP_ratio, self.logs_info_missing_file_dll_jars, self.TFP_DFP_ratio, self.no_of_valid_entry_points, self.no_of_valid_endpoints, self.no_of_exclusion, self.unanalyzed_code, self.missing_tables, self.no_of_tickets_to_make_ana_compliant_with_IMG, self.technology, self.extn_installed, self.use_case, self.tech_code_review])
                    
            else:
                with open(report_path, 'a') as f_object:
     
                    # Pass this file object to csv.writer()
                    # and get a writer object
                    writer_object = csv.writer(f_object)
                 
                    # Pass the list as an argument into
                    # the writerow()
                    writer_object.writerow([self.itrtn_no, self.application_name, self.start_date_time, self.end_date_time, self.no_of_scans_to_make_anlys_cmplnt_with_IMA, self.app_size_in_KLOC, self.artfct_cvrge_ratio, self.no_of_complex_trans,self.data_entities_by_trans,self.ratio_of_complete_trans_LOC, self.ratio_of_non_empty_trans, self.class_coverage_ratio, self.no_of_links, self.ratio_of_msg_que, self.ratio_of_soap_java_ope, self.ratio_of_rest_call, self.ratio_of_ope_call, self.no_of_unrev_dyn_lick, self.ratio_of_spring_mvc, self.ratio_of_typescript_angular_node_calls, self.AEFP_AETP_ratio, self.logs_info_missing_file_dll_jars, self.TFP_DFP_ratio, self.no_of_valid_entry_points, self.no_of_valid_endpoints, self.no_of_exclusion, self.unanalyzed_code, self.missing_tables, self.no_of_tickets_to_make_ana_compliant_with_IMG, self.technology, self.extn_installed, self.use_case, self.tech_code_review])
                 
                    # Close the file object
                    f_object.close()
        except Exception as e:
            print("Some exception has occurred while inserting into CSV File -> "+str(e))
        else:    
            print("Inserted data into IMG_INDICATORS CSV File.") 
            
            
            
        print("Inserting data into IMG_INDICATORS table......")
        try:  
            self.insertTable_IMG_INDICATORS(con, kb)
        except Exception as e:
            print("Some exception has occurred while inserting into table -> "+str(e))
        else:    
            print("Inserted data into IMG_INDICATORS table.")     

    def insertTable_IMG_INDICATORS(self, con, kb):
        # print("creating IMG_INDICATORS_Report_for_{}.csv ......".format(self.application_name))
        
        insert_table_query = """Insert into IMG_INDICATORS(itrtn_no, app_name, start_date_time, end_date_time, no_of_scans_to_make_anlys_cmplnt_with_IMA, app_size_in_KLOC, artfct_cvrge_ratio, no_of_complex_trans, data_entities_by_trans, ratio_of_complete_trans_LOC, ratio_of_non_empty_trans, class_coverage_ratio,  no_of_links, ratio_of_msg_que, ratio_of_soap_java_ope, ratio_of_rest_call, ratio_of_ope_call, no_of_unrev_dyn_lick, ratio_of_spring_mvc, ratio_of_typescript_angular_node_calls, AEFP_AETP_ratio, logs_info_missing_file_dll_jars, TFP_DFP_ratio, no_of_valid_entry_points, no_of_valid_endpoints, no_of_exclusion, unanalyzed_code, technology, extn_installed, tech_code_review) values  ("""+str(self.itrtn_no)+""", '"""+str(self.application_name)+"""', '"""+str(self.start_date_time)+"""', '"""+str(self.end_date_time)+"""', """+str(self.no_of_scans_to_make_anlys_cmplnt_with_IMA)+""", """+str(self.app_size_in_KLOC)+""", '"""+str(self.artfct_cvrge_ratio)+"""', """ +str(self.no_of_complex_trans)+""", """ +str(self.data_entities_by_trans)+""", """+str(self.ratio_of_complete_trans_LOC)+""", """+str(self.ratio_of_non_empty_trans)+""", """+str(self.class_coverage_ratio)+""", """+str(self.no_of_links)+""", '"""+str(self.ratio_of_msg_que) +"""' ,'"""+str(self.ratio_of_soap_java_ope)+"""' ,'"""+str(self.ratio_of_rest_call)+"""' ,'"""+str(self.ratio_of_ope_call)+"""',""" +str(self.no_of_unrev_dyn_lick)+""",'"""+str(self.ratio_of_spring_mvc)+"""','"""+str(self.ratio_of_typescript_angular_node_calls)+"""', """ +str(self.AEFP_AETP_ratio)+""", """+str(self.logs_info_missing_file_dll_jars)+""", """+str(self.TFP_DFP_ratio)+""", """+str(self.no_of_valid_entry_points)+""", """+str(self.no_of_valid_endpoints)+""", """+str(self.no_of_exclusion) +""", """+str(self.unanalyzed_code)+""", '"""+str(self.technology)+"""', '"""+str(self.extn_installed)+"""',"""+str(self.tech_code_review)+""");"""

        cursor = con.cursor()
        cursor.execute("SET search_path TO {}".format(kb))
        cursor.execute(insert_table_query)

        con.commit()

        # vm_name = socket.gethostname()
        vm_name = os.popen('hostname').read().strip()

        print("vm_name -> "+ vm_name)

        con_2 = psycopg2.connect(
            database= self.central_DB_name,
            user= self.central_DB_user,
            password= self.central_DB_password,
            host= self.central_DB_host,
            port= self.central_DB_port
        )

        cursor_2 = con_2.cursor()

        insert_table_query_central = """Insert into "Imaging_Indicator".IMG_INDICATORS_CENTRAL(itrtn_no, vm_name, app_name, start_date_time, end_date_time, no_of_scans_to_make_anlys_cmplnt_with_IMA, app_size_in_KLOC, artfct_cvrge_ratio, no_of_complex_trans, data_entities_by_trans, ratio_of_complete_trans_LOC, ratio_of_non_empty_trans, class_coverage_ratio,  no_of_links, ratio_of_msg_que, ratio_of_soap_java_ope, ratio_of_rest_call, ratio_of_ope_call, no_of_unrev_dyn_lick, ratio_of_spring_mvc, ratio_of_typescript_angular_node_calls, AEFP_AETP_ratio, logs_info_missing_file_dll_jars, TFP_DFP_ratio, no_of_valid_entry_points, no_of_valid_endpoints, no_of_exclusion, unanalyzed_code, technology, extn_installed, tech_code_review) values  ("""+str(self.itrtn_no)+""", '"""+str(vm_name)+"""', '"""+str(self.application_name)+"""', '"""+str(self.start_date_time)+"""', '"""+str(self.end_date_time)+"""', """+str(self.no_of_scans_to_make_anlys_cmplnt_with_IMA)+""", """+str(self.app_size_in_KLOC)+""", '"""+str(self.artfct_cvrge_ratio)+"""', """ +str(self.no_of_complex_trans)+""", """ +str(self.data_entities_by_trans)+""", """+str(self.ratio_of_complete_trans_LOC)+""", """+str(self.ratio_of_non_empty_trans)+""", """+str(self.class_coverage_ratio)+""", """+str(self.no_of_links)+""", '"""+str(self.ratio_of_msg_que) +"""' ,'"""+str(self.ratio_of_soap_java_ope)+"""' ,'"""+str(self.ratio_of_rest_call)+"""' ,'"""+str(self.ratio_of_ope_call)+"""',""" +str(self.no_of_unrev_dyn_lick)+""",'"""+str(self.ratio_of_spring_mvc)+"""','"""+str(self.ratio_of_typescript_angular_node_calls)+"""', """ +str(self.AEFP_AETP_ratio)+""", """+str(self.logs_info_missing_file_dll_jars)+""", """+str(self.TFP_DFP_ratio)+""", """+str(self.no_of_valid_entry_points)+""", """+str(self.no_of_valid_endpoints)+""", """+str(self.no_of_exclusion) +""", """+str(self.unanalyzed_code)+""", '"""+str(self.technology)+"""', '"""+str(self.extn_installed)+"""',"""+str(self.tech_code_review)+""");"""

        print("Inserting data into IMG_INDICATORS_CENTRAL table......")   
        cursor_2.execute(insert_table_query_central)
        con_2.commit()
        print("Inserted data into IMG_INDICATORS_CENTRAL table.")   
        
    def process(self, local_schema, central_schema, mngt_schema):
        try: 
            con = psycopg2.connect(
                database= self.local_DB_name,
                user= self.local_DB_user,
                password= self.local_DB_password,
                host= self.local_DB_host,
                port= self.local_DB_port
            )
            
            kb = local_schema
            print("kb->>" + str(kb)) 

            central = central_schema
            print("central->>" + str(central))

            mngt = mngt_schema
            print("mngt->>" + str(mngt))

            self.create_IMG_INDICATORS_table(con, kb)
            self.after_snapshot(con, self.application_name, kb, mngt, central)

        except Exception as e:
            print(traceback.format_exc())
        pass

    def get_application_guid(self, console_url, console_username, console_password, app_name):
        if console_url.endswith('/'):
            url=f"{console_url}api/applications"
        else:
            url=f"{console_url}/api/applications"

        auth = HTTPBasicAuth(console_username, console_password)

        try:
            #fetching the Application list and details.
            rsp = requests.get(url, auth=auth)
            # print(rsp.status_code)
            if rsp.status_code == 200:
                apps = json.loads(rsp.text) 
                for app in apps['applications']:
                    if app["name"] == app_name:
                        return app["guid"] 
                print(f'{app_name} application not present in AIP Console')

            else:
                print("Some error has occured! ")
                print(rsp.text)

        except Exception as e:
            print('some exception has occured! \n Please resolve them or contact developers')
            print(e)

    def get_app_schemas(self, console_url, console_username, console_password, guid):
        if console_url.endswith('/'):
            url=f"{console_url}api/aic/applications/{guid}"
        else:
            url=f"{console_url}/api/aic/applications/{guid}"

        auth = HTTPBasicAuth(console_username, console_password)

        try:
            #fetching the app schemas.
            rsp = requests.get(url, auth=auth)
            # print(rsp.status_code)
            if rsp.status_code == 200:
                data = json.loads(rsp.text) 

                for i in range(len(data["schemas"])):
                    if data["schemas"][i]["type"] == 'local':
                        local_schema = data["schemas"][i]["name"]
                    if data["schemas"][i]["type"] == 'central':
                        central_schema = data["schemas"][i]["name"]
                    if data["schemas"][i]["type"] == 'management':
                        mngt_schema = data["schemas"][i]["name"]
                return local_schema, central_schema, mngt_schema  

            else:
                print("Some error has occured! ")
                print(rsp.text)

        except Exception as e:
            print('some exception has occured! \n Please resolve them or contact developers')
            print(e)


if __name__ == "__main__":
    
    application_name = sys.argv[1]
    local_DB_name= sys.argv[2] 
    local_DB_host = sys.argv[3] 
    local_DB_port = sys.argv[4] 
    local_DB_user = sys.argv[5]
    local_DB_password = sys.argv[6] 

    console_url = sys.argv[7] 
    console_username = sys.argv[8] 
    console_password = sys.argv[9]

    central_DB_name = sys.argv[10]
    central_DB_host = sys.argv[11]
    central_DB_port = sys.argv[12]
    central_DB_user= sys.argv[13]
    central_DB_password= sys.argv[14]
            
    # application_name = 'webgoat_v8_2_2'
    # local_DB_name= 'postgres'
    # local_DB_host = 'localhost'
    # local_DB_port = '2284' 
    # local_DB_user = 'operator'
    # local_DB_password = 'CastAIP'

    # console_url = 'http://localhost:8081/'
    # console_username = 'admin' 
    # console_password = 'admin'

    # central_DB_name = 'postgres'
    # central_DB_host = 'tooling3'
    # central_DB_port = '2284'
    # central_DB_user= 'operator'
    # central_DB_password = 'CastAIP'

    onb_obj = Report(application_name, local_DB_name, local_DB_host, local_DB_port, local_DB_user, local_DB_password, console_url, console_username, console_password, central_DB_name, central_DB_host, central_DB_port, central_DB_user, central_DB_password)
   
    app_guid = onb_obj.get_application_guid(console_url, console_username, console_password, application_name)
   
    local_schema, central_schema, mngt_schema = onb_obj.get_app_schemas(console_url, console_username, console_password, app_guid)
    onb_obj.process(local_schema, central_schema, mngt_schema)

