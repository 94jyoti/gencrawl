# gencrawl

For running listing spider - 

`scrapy crawl financial_listing -a config="pgim_com" -o res/pgim_com.jl`
See config file configuration for listing at - configs/pgim_com.json`


For running detail spider to test some urls - 

`scrapy crawl financial_detail_pgim_com -a config=pgim_com -a 
urls="https://www.pgim.com/investments/mutual-funds/pgim-absolute-return-bond-fund|https://www.pgim.com/investments/mutual-funds/pgim-tips-fund"
-o pgim_test.csv`

For running detail spider taking input from file - 

`scrapy crawl financial_detail_pgim_com -a config=pgim_com -a input_file=pgim_com.jl -o pgim_all_data.jl`


Converting jl to csv
`python bin/json_to_csv.py /home/sagar/Documents/forage/gencrawl/pgim.jl`