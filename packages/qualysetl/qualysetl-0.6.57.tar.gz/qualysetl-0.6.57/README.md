# Example Code from [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series)

BETA Release of Example code from the [Qualys API Best Practices Series](https://blog.qualys.com/tag/api-best-practices-series) 
enhanced with some packaging and operational capability. 
> This example code is being actively developed at Qualys to help customers Extract, Transform and Load Qualys
> data into JSON, CSV (Excel), and SQLite Database that can be distributed locally or into the cloud. 
> See [Roadmap](#roadmap) for additional details.

### Workflow Diagram
The workflow depicts the flow of etl for host list detection.  The key output is the sqlite database that is ready for distribution
- qetl_manage_user -u [userdir] -e etl_host_list_detection -d [datetime] - Resulting sqlite database ready for distribution.

[![](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)](https://user-images.githubusercontent.com/82658653/122486769-b817fd00-cfa7-11eb-9f71-2cd01101e006.png)

### Component Diagram
The component diagram depicts major system interoperability components that deliver data into the enterprise.  

See [qualys_etl directory](/qualys_etl#readme) for details.

[![](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)](https://user-images.githubusercontent.com/82658653/120926641-c1ea5800-c6ab-11eb-832b-1af03f77462a.png)




