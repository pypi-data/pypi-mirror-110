# Example Code from [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series)

BETA Release of Example code from the [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series) 
enhanced with some packaging and operational capability. 
> An accompanying video will be available from Qualys by June 25th, 2021, Part 3 - Host List Detection.   
> - Hold off on using until the Part 3 video is released as part of [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series)
> - See [Roadmap](#roadmap) for additional details.  

> <b>Example: ETL Host List Detection Data</b>
> - qetl_manage_user -u [path] -e etl_host_list_detection
>>     - create csv, json and sqlite from Host List Detection Endpoint
>>     - sqlite will contain three tables:  
>>
>>       1) Q_Host_List_Detection - Host List Detection Data from vm_processed_after - utc.now to now
>>          - Host List Detection Endpoint: 
>>            /api/2.0/fo/asset/host/vm/detection/?action=list
>>
>>       2) Q_Host_List - Host List Data from vm_processed_after to now
>>          - Host List Endpoint:
>>            /api/2.0/fo/asset/host/?action=list
>>
>>       3) Q_KnowledgeBase_In_Host_List_Detection - corresponding QIDs from Q_Host_List_Detection
>>          - KnowledgeBase Endpoint:  
>>            /api/2.0/fo/knowledge_base/vuln/?action=list
>>
> ### Output - Host List Detection SQLite Database Tables 
> 
> [![](https://user-images.githubusercontent.com/82658653/122657081-3dc5b500-d12e-11eb-8f4d-a4ccfd365f47.png)](https://user-images.githubusercontent.com/82658653/122657081-3dc5b500-d12e-11eb-8f4d-a4ccfd365f47.png)


### Workflow Diagram
The workflow depicts the flow of etl for host list detection.  The key output is the sqlite database that is ready for distribution
- qetl_manage_user -u [userdir] -e etl_host_list_detection -d [datetime] - Resulting sqlite database ready for distribution.

[![](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)

### Component Diagram
The component diagram depicts major system interoperability components that deliver data into the enterprise.  

See [qualys_etl directory](/qualys_etl#readme) for details.

[![](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)




