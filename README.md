# gencrawl

[comment]: <> (For running listing spider - )

[comment]: <> (`scrapy crawl financial_listing -a config="pgim_com" -o res/pgim_com.jl`)

[comment]: <> (See config file configuration for listing at - configs/pgim_com.json`)


For running NFN spider - 

`scrapy crawl financial_detail_pgim_com -a config=pgim_com -a client=NFN`



For running a DHC spider - 
`scrapy crawl hospital_detail -a config=hospital_detail_sheridanhospital_org_us -a client=DHC`     

For running a DHC spider with sample urls - 
`scrapy crawl hospital_detail -a config=hospital_detail_sheridanhospital_org_us -a client=DHC -a urls="url1|url2"`

For running a DHC spider with db urls - 
`scrapy crawl hospital_detail -a config=hospital_detail_sheridanhospital_org_us -a client=DHC -a db_limit=50`


Converting jl to csv
`python bin/json_to_csv.py /home/sagar/Documents/forage/gencrawl/pgim.jl`

Deploying project on Zyte server
`shub image build nfn`
`shub image push nfn`
`shub image deploy nfn`