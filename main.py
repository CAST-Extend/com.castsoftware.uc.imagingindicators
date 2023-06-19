import os
import time
import xlsxwriter
from cast.application import Server, ApplicationLevelExtension, create_postgres_engine
# from tkinter.font import BOLD
import logging


class Report(ApplicationLevelExtension):


    def __init__(self):
        self.itrtn_no = 0
        self.app_name = 'NULL'
        self.current_date_time= 'NULL'
        self.no_of_scans_to_make_anlys_cmplnt_with_IMA = 0
        self.app_size_in_KLOC = 0.0
        self.artfct_cvrge_ratio = 0
        self.no_of_complete_trans = 0
        self.data_entities_by_trans = 0
        self.ratio_of_complete_trans_LOC = 0.0
        self.ratio_of_non_empty_trans = 0
        self.class_coverage_ratio = 0.0
        self.prog_in_trans = 0.0
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

    
    def start_application(self, application):
        """
        Called before analysis.
        
        .. versionadded:: CAIP 8.3
        
        :type application: :class:`cast.application.Application`
        @type application: cast.application.Application
        """
        
        logging.info('start_application........................................................................')
        

        pass
    
    def end_application(self, application):
        """
        Called at the end of application's analysis.

        :type application: :class:`cast.application.Application`
        @type application: cast.application.Application
        """
        logging.info('end_application............................................................................')

        
        logging.info("creating table IMG_INDICATORS.......")

        try:
            
            create_table_query = """CREATE TABLE IF NOT EXISTS IMG_INDICATORS( itrtn_no INT, app_name VARCHAR(100), current_date_time VARCHAR(100),
            no_of_scans_to_make_anlys_cmplnt_with_IMA INT, app_size_in_KLOC FLOAT, artfct_cvrge_ratio INT, no_of_complete_trans  INT, 
            data_entities_by_trans INT, ratio_of_complete_trans_LOC FLOAT, ratio_of_non_empty_trans INT, class_coverage_ratio FLOAT, 
            prog_in_trans FLOAT, no_of_links INT, ratio_of_msg_que VARCHAR(50), ratio_of_soap_java_ope VARCHAR(50), ratio_of_rest_call VARCHAR(50),
            ratio_of_ope_call VARCHAR(50), no_of_unrev_dyn_lick INT, ratio_of_spring_mvc VARCHAR(50), ratio_of_typescript_angular_node_calls VARCHAR(50), 
            AEFP_AETP_ratio INT, logs_info_missing_file_dll_jars VARCHAR(1000), TFP_DFP_ratio INT, no_of_valid_entry_points INT, 
            no_of_valid_endpoints INT, no_of_exclusion INT, unanalyzed_code INT, missing_tables INT, no_of_tickets_to_make_ana_compliant_with_IMG INT, 
            technology VARCHAR(1000), extn_installed VARCHAR(10000), use_case INT, tech_code_review INT);"""

            application.sql_tool(create_table_query)

        except Exception as e:
            logging.info("Some exception has occurred while creating table -> "+str(e))

        else:    
            logging.info("created table IMG_INDICATORS.")
        

        pass

    def after_module(self, application):
        """
        Called after module content creation.
        
        .. versionadded:: CAIP 8.3
        
        :type application: :class:`cast.application.Application`
        @type application: cast.application.Application
        """
        logging.info('after_module............................................................................')
        pass

    def after_snapshot(self, application):
        """
        Called after module content creation.
        Gives you the central's application.
        
        .. versionadded:: CAIP 8.3
        
        :type application: :class:`cast.application.central.Application`        
        @type application: cast.application.central.Application
        """
        # if self.counter !=0:
        #     return
        # else:
        #     self.counter= self.counter+1
        logging.info('after_snapshot........................................................................')


        
        kb = application.get_application_configuration().get_analysis_service()
        # kb = application.get_knowledge_base()
        logging.info('kb -> '+str(kb))
        mngt = application.get_managment_base()
        logging.info('mngt -> '+str(mngt))
        central = application.get_central()
        logging.info('central -> '+str(central))
        # eng = create_postgres_engine(user='operator',
        #                    password='CastAIP',
        #                    host='localhost',
        #                    port=2284,
        #                    database='postgres')
        # server = Server(eng)
        # schemas = server._get_all_schemas()        
        # central_schemas = []
        # # logging.info('app name -> '+str(application.get_name()))
        # for i in schemas:
        #     if i.endswith("central"):
        #         central_schemas.append(i)
        # # print('central_schemas -> '+str(central_schemas))       
        # app_name = application.get_name()
        # central_schema = ''
        # for i in central_schemas:
        #     if app_name == i[:-8]:
        #         central_schema = i               
        # # logging.info('central_schema -> '+str(central_schema))
        # central = server.get_schema(central_schema)
        
        try:
            for line in kb.execute_query("""SELECT itrtn_no FROM img_indicators ORDER BY itrtn_no DESC LIMIT 1;"""):
                self.itrtn_no = int(line[0]) + 1
                if self.itrtn_no is None:
                    self.itrtn_no = 0
                
        except Exception as e:
            self.itrtn_no = 0

        logging.info('itrtn_no -> '+str(self.itrtn_no))
        
        self.app_name = application.name
        logging.info('app_name -> '+str(self.app_name))
        
        self.current_date_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        logging.info('current_date_time -> '+str(self.current_date_time))
        
        for line in mngt.execute_query("""select count(*) from tasklog_history where lower(log_context) like lower('%Execute_Analysis%MainTask_SummaryLog%')"""):
            self.no_of_scans_to_make_anlys_cmplnt_with_IMA = line[0]
            if self.no_of_scans_to_make_anlys_cmplnt_with_IMA is None:
                self.no_of_scans_to_make_anlys_cmplnt_with_IMA = 0
            logging.info('no_of_scans_to_make_anlys_cmplnt_with_IMA -> '+str(self.no_of_scans_to_make_anlys_cmplnt_with_IMA))    

        for line in central.execute_query("""select dmr.metric_num_value from dss_metric_results dmr, dss_metric_types dmt, dss_objects o 
        where dmr.metric_id = dmt.metric_id and dmr.object_id = o.object_id and o.object_type_id = -102 and snapshot_id = (select max(snapshot_id) from dss_snapshots) and 
        (dmr.metric_value_index = 1 and dmr.metric_id in (10151))"""):
            self.app_size_in_KLOC = line[0]
            if self.app_size_in_KLOC is None or self.app_size_in_KLOC is '':
                self.app_size_in_KLOC = 0.0
            logging.info('app_size_in_KLOC -> '+str(self.app_size_in_KLOC))
                   
        for line in kb.execute_query("""select count(*) from (select 'Artifact Coverage' as check_description, 
        cast(total_count as text) as compute_value2, cast(covered_count as text) as compute_value1,
        cast((covered_count*100/ case when total_count = 0 then 1 else total_count end)as text) ||'%' as percentage_ratio, 
        CASE when cast((covered_count*100/ case when total_count = 0 then 1 else total_count end)as integer) <= 30 THEN 'RED' 
        when ( cast((covered_count*100/ case when total_count = 0 then 1 else total_count end)as integer) <= 50 and cast((covered_count*100/
        case when total_count = 0 then 1 else total_count end)as integer) > 30 ) THEN 'AMBER' when cast((covered_count*100/
        case when total_count = 0 then 1 else total_count end)as integer) > 50 THEN 'GREEN' end as rag from
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
        ,'VB MDI Form','SHELL Program','ColdFusion Template','C/C++ File','C# Class','Java Class','VB Module','Session')) covered) as art;"""):
            self.artfct_cvrge_ratio = line[0]
            if self.artfct_cvrge_ratio is None:
                artfct_cvrge_ratio = 0
            logging.info('artfct_cvrge_ratio -> '+str(self.artfct_cvrge_ratio) )
        
        for line in kb.execute_query("""select count(1) from dss_transactiondetails"""):
            self.no_of_complete_trans = line[0]
            if self.no_of_complete_trans is None:
                self.no_of_complete_trans = 0
            logging.info('no_of_complete_trans -> '+str(self.no_of_complete_trans) )
            
        for line in kb.execute_query("""select count(object_id) from cdt_objects where lower(object_type_str) like '%table%' and object_id in 
        (select child_id from dss_transactiondetails);"""):
            self.data_entities_by_trans = line[0]
            if self.data_entities_by_trans is None:
                self.data_entities_by_trans = 0
            logging.info('data_entities_by_trans -> '+str(self.data_entities_by_trans))
        
        for line in kb.execute_query("""select round((afp.fp:: float/codelines.LOC :: float), 2)
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
        (select sum(ilf_ex) as df from dss_datafunction where cal_flags = 0) as dfp) as afp;"""):
            self.ratio_of_complete_trans_LOC = line[0]
            if self.ratio_of_complete_trans_LOC is None:
                self.ratio_of_complete_trans_LOC = 0
            logging.info('ratio_of_complete_trans_LOC -> '+str(self.ratio_of_complete_trans_LOC))
            
        for line in kb.execute_query("""select cast( ((tb_empty_tr.tr_count  * 100)/ nullif(tb_all_tr.tr_count,0)) as text) as percentage_ratio
        from (select count(cob.object_name) as tr_count from dss_transaction dtr, cdt_objects cob
        where dtr.form_id = cob.object_id and dtr.cal_mergeroot_id = 0  and dtr.cal_flags not in (  8, 10, 126, 128,136, 138, 256, 258 ) ) tb_all_tr,
        (select count(cob.object_name) as tr_count from dss_transaction dtr, cdt_objects cob where dtr.form_id = cob.object_id and dtr.cal_mergeroot_id = 0  
        and dtr.cal_flags not in (  8, 10, 126, 128,136, 138, 256, 258 )  and DTR.tf_ex=0  ) tb_empty_tr;"""):
            self.ratio_of_non_empty_trans = line[0]
            if self.ratio_of_non_empty_trans is None:
                self.ratio_of_non_empty_trans = 0
            logging.info('ratio_of_non_empty_trans -> '+str(self.ratio_of_non_empty_trans))
            
        for line in central.execute_query("""select  cast(fp_to_pgmclass_ratio as text) as percentage_ratio from(
        select pgm_classes.pgm_count Programs_Class, fp_count.fp FP, round(CASE WHEN pgm_classes.pgm_count = 0::numeric THEN 0::numeric
        ELSE fp_count.fp / pgm_classes.pgm_count END, 2) AS fp_to_pgmclass_ratio from 
        (select sum(metric_num_value) as pgm_count from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10155, 10156)) as pgm_classes,
        (select sum(metric_num_value) as fp from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 and t1.snapshot_id = 
        (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10203, 10204)) as fp_count ) as dataTable """):
            self.class_coverage_ratio = line[0]
            if self.class_coverage_ratio is None:
                class_coverage_ratio = 0.0
            logging.info('class_coverage_ratio -> '+str(self.class_coverage_ratio))       
        
        for line in central.execute_query("""select cast(fp_to_pgmclass_ratio as text) as percentage_ratio from(
        select pgm_classes.pgm_count Programs_Class, fp_count.fp FP, 
        round( CASE WHEN pgm_classes.pgm_count = 0::numeric THEN 0::numeric 
        ELSE fp_count.fp / pgm_classes.pgm_count END, 2) AS fp_to_pgmclass_ratio  from 
        (select sum(metric_num_value) as pgm_count from dss_metric_results t1, dss_metric_types t2, 
        dss_objects t3 where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots) and t1.metric_id in ( 10155, 10156)) as pgm_classes,
        (select sum(metric_num_value) as fp from dss_metric_results t1, dss_metric_types t2, dss_objects t3
        where t1.metric_id = t2.metric_id and t1.object_id = t3.object_id and t3.object_type_id = -102 
        and t1.snapshot_id = (select max(snapshot_id) from dss_snapshots)
        and t1.metric_id in ( 10203, 10204)) as fp_count ) as dataTable """):
            self.prog_in_trans = line[0]
            if self.prog_in_trans is None:
                prog_in_trans = 0
            logging.info('prog_in_trans -> '+str(self.prog_in_trans))
        
        for line in kb.execute_query("""select count(1) from CTV_links;"""):
            self.no_of_links = line[0]
            if self.no_of_links is None:
                self.no_of_links = 0
            logging.info('no_of_links -> '+str(self.no_of_links))
            
        for line in kb.execute_query("""select CONCAT(( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('IBM MQ Java Queue Publisher', 'IBM MQ Java Queue Receiver', 'IBM MQ Java Topic Publisher', 'IBM MQ Java Topic Receiver', 'IBM MQ Java Unknown Queue Publisher', 'IBM MQ Java Unknown Queue Receiver', 'IBM MQ Java Unknown Topic Publisher', 'IBM MQ Java Unknown Topic Receiver', 'Java AWS Simple Queue Service Publisher', 'Java AWS Simple Queue Service Receiver', 'Java AWS Simple Queue Service Unknown Publisher', 'Java AWS Simple Queue Service Unknown Receiver', 'JMS Java Queue Publisher', 'JMS Java Queue Receiver', 'JMS Java Topic Publisher', 'JMS Java Topic Receiver', 'JMS Java Unknown Queue Publisher', 'JMS Java Unknown Queue Receiver', 'JMS Java Unknown Topic Publisher', 'JMS Java Unknown Topic Receiver', 'RabbitMQ Java Queue Publisher', 'RabbitMQ Java Queue Receiver', 'RabbitMQ Unknown Java Queue Publisher', 'RabbitMQ Unknown Java Queue Receiver')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1 where co1.object_type_str in ('IBM MQ Java Queue Publisher', 'IBM MQ Java Queue Receiver', 'IBM MQ Java Topic Publisher', 'IBM MQ Java Topic Receiver', 'IBM MQ Java Unknown Queue Publisher', 'IBM MQ Java Unknown Queue Receiver', 'IBM MQ Java Unknown Topic Publisher', 'IBM MQ Java Unknown Topic Receiver', 'Java AWS Simple Queue Service Publisher', 'Java AWS Simple Queue Service Receiver', 'Java AWS Simple Queue Service Unknown Publisher', 'Java AWS Simple Queue Service Unknown Receiver', 'JMS Java Queue Publisher', 'JMS Java Queue Receiver', 'JMS Java Topic Publisher', 'JMS Java Topic Receiver', 'JMS Java Unknown Queue Publisher', 'JMS Java Unknown Queue Receiver', 'JMS Java Unknown Topic Publisher', 'JMS Java Unknown Topic Receiver', 'RabbitMQ Java Queue Publisher', 'RabbitMQ Java Queue Receiver', 'RabbitMQ Unknown Java Queue Publisher', 'RabbitMQ Unknown Java Queue Receiver')))"""):
            self.ratio_of_msg_que = line[0]
            if self.ratio_of_msg_que is None:
                ratio_of_msg_que = 'null'
            logging.info('ratio_of_msg_que -> '+str(self.ratio_of_msg_que))
            
        for line in kb.execute_query("""select CONCAT((select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('SOAP Client end point', 'SOAP Java Client', 'SOAP Java Client Operation', 'SOAP Java Operation', 'SOAP Java Port Type', 'SOAP Java Web Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1 where co1.object_type_str in ('SOAP Client end point', 'SOAP Java Client', 'SOAP Java Client Operation', 'SOAP Java Operation', 'SOAP Java Port Type', 'SOAP Java Web Service')))"""):
            self.ratio_of_soap_java_ope = line[0]
            if self.ratio_of_soap_java_ope is None:
                ratio_of_soap_java_ope = 'null'
            logging.info('ratio_of_soap_java_ope -> '+str(self.ratio_of_soap_java_ope))
            
        for line in kb.execute_query("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Patch Resource Service', 'Delete Resource Service', 'Get Resource Service', 'Post Resource Service', 'Put Resource Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Patch Resource Service', 'Delete Resource Service', 'Get Resource Service', 'Post Resource Service', 'Put Resource Service')))"""):
            self.ratio_of_rest_call = line[0]
            if self.ratio_of_rest_call is None:
                self.ratio_of_rest_call = 'null'
            logging.info('ratio_of_rest_call -> '+str(self.ratio_of_rest_call))
              
        for line in kb.execute_query("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('JAX-RS Delete Operation Service', 'JAX-RS Get Operation Service', 'JAX-RS Get Resource Service', 'JAX-RS Post Operation Service', 'JAX-RS Put Operation Service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('JAX-RS Delete Operation Service', 'JAX-RS Get Operation Service', 'JAX-RS Get Resource Service', 'JAX-RS Post Operation Service', 'JAX-RS Put Operation Service')))"""):
            self.ratio_of_ope_call = line[0]
            if self.ratio_of_ope_call is None:
                self.ratio_of_ope_call = 'null'
            logging.info('ratio_of_ope_call -> '+str(self.ratio_of_ope_call))
        
        for line in kb.execute_query("""Select count(prop) from acc where prop = 1;"""):
            self.no_of_unrev_dyn_lick = line[0]
            if self.no_of_unrev_dyn_lick is None:
                self.no_of_unrev_dyn_lick = 0
            logging.info('no_of_unrev_dyn_lick -> '+str(self.no_of_unrev_dyn_lick))
        
        for line in kb.execute_query("""select CONCAT((select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Spring MVC Any Operation', 'Spring MVC Delete Operation', 'Spring MVC Get Operation', 'Spring MVC Post Operation', 'Spring MVC Put Operation', 'Spring MVC Service', 'Thymeleaf DELETE resource service', 'Thymeleaf GET resource service', 'Thymeleaf POST resource service', 'Thymeleaf PUT resource service')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Spring MVC Any Operation', 'Spring MVC Delete Operation', 'Spring MVC Get Operation', 'Spring MVC Post Operation', 'Spring MVC Put Operation', 'Spring MVC Service', 'Thymeleaf DELETE resource service', 'Thymeleaf GET resource service', 'Thymeleaf POST resource service', 'Thymeleaf PUT resource service')))"""):
            self.ratio_of_spring_mvc = line[0]
            if self.ratio_of_spring_mvc is None:
                self.ratio_of_spring_mvc = 'null'
            logging.info('ratio_of_spring_mvc -> '+str(self.ratio_of_spring_mvc))
        
        for line in kb.execute_query("""select CONCAT( ( select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Angular GET http service', 'TypeScript GET http service', 'Angular POST http service', 'TypeScript POST http service', 'Angular PUT http service', 'TypeScript PUT http service', 'Angular DELETE http service', 'TypeScript DELETE http service', 'Node.js Delete Operation Service', 'Node.js Get Operation Service', 'Node.js Post Operation Service', 'Node.js Put Operation Service', 'Node.js MongoDB connection', 'Node.js MongoDB collection', 'Node.js AWS SQS Publisher', 'Node.js AWS SQS', 'Node.js AWS SQS Unknown Publisher', 'Node.js AWS SQS Unknown', 'Node.js AWS SNS Publisher', 'Node.js AWS SNS Subscriber', 'Node.js AWS SNS Unknown Publisher', 'Node.js AWS SNS Unknown Subscriber', 'Node.js AWS Lambda Post Operation Service', 'Node.js AWS Lambda Put Operation Service', 'Node.js AWS Lambda Delete Operation Service', 'Node.js AWS Lambda Any Operation Service', 'Node.js Call to Lambda', 'Node.js Call to unknown Lambda')
        and co1.object_id in (select caller_id from ctv_links cl1 where cl1.caller_id=co1.object_id )
        and co1.object_id in (select called_id from ctv_links cl1 where cl1.called_id=co1.object_id ))
        , ' / ', 
        (select count(co1.object_id) from cdt_objects co1
        where co1.object_type_str in ('Angular GET http service', 'TypeScript GET http service', 'Angular POST http service', 'TypeScript POST http service', 'Angular PUT http service', 'TypeScript PUT http service', 'Angular DELETE http service', 'TypeScript DELETE http service', 'Node.js Delete Operation Service', 'Node.js Get Operation Service', 'Node.js Post Operation Service', 'Node.js Put Operation Service', 'Node.js MongoDB connection', 'Node.js MongoDB collection', 'Node.js AWS SQS Publisher', 'Node.js AWS SQS', 'Node.js AWS SQS Unknown Publisher', 'Node.js AWS SQS Unknown', 'Node.js AWS SNS Publisher', 'Node.js AWS SNS Subscriber', 'Node.js AWS SNS Unknown Publisher', 'Node.js AWS SNS Unknown Subscriber', 'Node.js AWS Lambda Post Operation Service', 'Node.js AWS Lambda Put Operation Service', 'Node.js AWS Lambda Delete Operation Service', 'Node.js AWS Lambda Any Operation Service', 'Node.js Call to Lambda', 'Node.js Call to unknown Lambda')))"""):
            self.ratio_of_typescript_angular_node_calls = line[0]
            if self.ratio_of_typescript_angular_node_calls is None:
                self.ratio_of_typescript_angular_node_calls = 'null'
            logging.info('ratio_of_typescript_angular_node_calls -> '+str(self.ratio_of_typescript_angular_node_calls))
        
        for line in kb.execute_query("""select count (*) from (select c1.metric_num_value as current_aefp , c2.metric_num_value as current_aetp, 
        c3.metric_num_value as previous_aefp,c4.metric_num_value as previous_aetp , case when c4.metric_num_value <> 0 
        then round(((c2.metric_num_value -c4.metric_num_value)/ c4.metric_num_value)*100,2) else 0 end varPercent  
        from   dss_metric_results c1, dss_metric_results c2,dss_metric_results c3, dss_metric_results c4  
        where c1.metric_id  = 10430 and c2.metric_id = 10440  and c3.metric_id  = 10430 and c4.metric_id = 10440  and c1.object_id in 
        (select object_id from dss_objects where object_type_id =-102)   and c2.object_id in (select object_id from dss_objects where object_type_id =-102)  and c1.snapshot_id = 
        (select max(snapshot_id) from dss_snapshots)  and c2.snapshot_id = (select max(snapshot_id) from dss_snapshots)  and c3.snapshot_id = 
        (select snapshot_id from (select snapshot_id from dss_snapshots order by snapshot_id desc limit 2) as snapid 
        order by snapshot_id limit 1) and c3.object_id in (select object_id from dss_objects where object_type_id =-102)   
        and c4.object_id in (select object_id from dss_objects where object_type_id =-102)  and c4.snapshot_id = 
        (select snapshot_id from (select snapshot_id from dss_snapshots order by snapshot_id desc limit 2) as snapid order by snapshot_id limit 1)) as t"""):
            self.AEFP_AETP_ratio = line[0]
            if self.AEFP_AETP_ratio is None:
                self.AEFP_AETP_ratio = 0
            logging.info('AEFP_AETP_ratio -> '+str(self.AEFP_AETP_ratio))

        for line in kb.execute_query("""select cast((TFP + .0001)/(DFP +.0001) as text) as percentage_ratio
        from (select sum(DTR.tf_ex) as TFP from dss_transaction dtr, cdt_objects cob where dtr.form_id = cob.object_id
        and dtr.cal_mergeroot_id = 0 and dtr.cal_flags not in ( 8, 10, 126, 128,136, 138, 256, 258 ) ) as TFP,
        ( select sum(dtf.ilf_ex) as DFP from dss_datafunction dtf, cdt_objects cob where dtf.maintable_id = cob.object_id and dtf.cal_flags in (0,2)) as DFP;"""):
            self.TFP_DFP_ratio = line[0]
            if self.TFP_DFP_ratio is None:
                self.TFP_DFP_ratio = 0
            logging.info('TFP_DFP_ratio -> '+str(self.TFP_DFP_ratio))

            
        for line in kb.execute_query("""select count(distinct(cdt.object_type_str)) from cdt_objects cdt, dss_transaction dt
        where dt.cal_flags = 0 and dt.form_id = cdt.object_id"""):
            self.no_of_valid_entry_points = line[0]
            if self.no_of_valid_entry_points is None:
                self.no_of_valid_entry_points = 0
            logging.info('no_of_valid_entry_points -> '+str(self.no_of_valid_entry_points))
         
        for line in kb.execute_query("""select count(distinct(cdt.object_type_str))
        from cdt_objects cdt, fp_dataendpoints de where cdt.object_id = de.object_id"""):
            self.no_of_valid_endpoints = line[0]
            if self.no_of_valid_endpoints is None:
                self.no_of_valid_endpoints = 0
            logging.info('no_of_valid_endpoints -> '+str(self.no_of_valid_endpoints))
        
        for line in kb.execute_query("""select  count(distinct(cdt.object_type_str))
        from cdt_objects cdt, fp_result_excludedobjects fre where cdt.object_id = fre.object_id"""):
            self.no_of_exclusion = line[0]
            if self.no_of_exclusion is None:
                self.no_of_exclusion = 0
            logging.info('no_of_exclusion -> '+str(self.no_of_exclusion))
        
        for line in kb.execute_query("""SELECT STRING_AGG(distinct(object_language_name), ', ') FROM cdt_objects where object_language_name not like '%N/A%'"""):
            self.technology = line[0]
            if self.technology is None:
                self.technology = 'null'
            logging.info('technology -> '+str(self.technology))
            
        for line in kb.execute_query("""select STRING_AGG(distinct(package_name), ', ') from sys_package_version where package_name like '%com%'"""):
            self.extn_installed = line[0]
            if self.extn_installed is None:
                self.extn_installed = 'null'
            logging.info('extn_installed -> '+str(self.extn_installed))
            
        for line in central.execute_query("""SELECT COUNT(1) AS "ARTIFACTS_NOT_CONTRIBUTING_TO_FP"
        FROM AEP_TECHNICAL_ARTIFACTS_VW A JOIN DSS_OBJECTS O ON A.OBJECT_ID = O.OBJECT_ID """):
            self.tech_code_review = line[0]
            if self.tech_code_review is None:
                self.tech_code_review = 0
            logging.info('tech_code_review -> '+str(self.tech_code_review))
            

        logging.info("Inserting data into IMG_INDICATORS table......")
        try:  
            self.insertTable_IMG_INDICATORS(kb)
        except Exception as e:
            logging.info("Some exception has occurred while inserting into table -> "+str(e))
        else:    
            logging.info("Inserted data into IMG_INDICATORS table.")   

    def insertTable_IMG_INDICATORS(self, kb):

        cr = kb.create_cursor()
        insert_table_query = """Insert into IMG_INDICATORS(itrtn_no, app_name, current_date_time, no_of_scans_to_make_anlys_cmplnt_with_IMA, app_size_in_KLOC, artfct_cvrge_ratio, no_of_complete_trans, data_entities_by_trans, ratio_of_complete_trans_LOC, ratio_of_non_empty_trans, class_coverage_ratio, prog_in_trans, no_of_links, ratio_of_msg_que, ratio_of_soap_java_ope, ratio_of_rest_call, ratio_of_ope_call, no_of_unrev_dyn_lick, ratio_of_spring_mvc, ratio_of_typescript_angular_node_calls, AEFP_AETP_ratio, no_of_valid_entry_points, no_of_valid_endpoints, no_of_exclusion, technology, extn_installed, tech_code_review) values  ("""+str(self.itrtn_no)+""", '"""+str(self.app_name)+"""', '"""+str(self.current_date_time)+"""', """+str(self.no_of_scans_to_make_anlys_cmplnt_with_IMA)+""", """+str(self.app_size_in_KLOC)+""", """+str(self.artfct_cvrge_ratio)+""", """ +str(self.no_of_complete_trans)+""", """ +str(self.data_entities_by_trans)+""", """+str(self.ratio_of_complete_trans_LOC)+""", """+str(self.ratio_of_non_empty_trans)+""", """+str(self.class_coverage_ratio)+""", """+str(self.prog_in_trans)+""", """+str(self.no_of_links)+""", '"""+str(self.ratio_of_msg_que) +"""' ,'"""+str(self.ratio_of_soap_java_ope)+"""' ,'"""+str(self.ratio_of_rest_call)+"""' ,'"""+str(self.ratio_of_ope_call)+"""',""" +str(self.no_of_unrev_dyn_lick)+""",'"""+str(self.ratio_of_spring_mvc)+"""','"""+str(self.ratio_of_typescript_angular_node_calls)+"""', """ +str(self.AEFP_AETP_ratio)+""", """+str(self.no_of_valid_entry_points)+""", """+str(self.no_of_valid_endpoints)+""", """+str(self.no_of_exclusion) +""", '"""+str(self.technology)+"""', '"""+str(self.extn_installed)+"""',"""+str(self.no_of_valid_endpoints)+""");"""
        
        kb._execute_raw_query(cr, insert_table_query)    
