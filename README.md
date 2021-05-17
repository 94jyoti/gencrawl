# gencrawl

For running listing spider - 

`scrapy crawl financial_listing -a config="pgim_com" -o res/pgim_com.jl`
See config file configuration for listing at - configs/pgim_com.json`


For running detail spider to test some urls - 

`scrapy crawl financial_detail_pgim_com -a config=pgim_com -a 
urls="https://www.pgim.com/investments/mutual-funds/pgim-absolute-return-bond-fund|https://www.pgim.com/investments/mutual-funds/pgim-tips-fund"
-o pgim_test.csv`

For taking input from file - 

`scrapy crawl financial_detail_pgim_com -a config=pgim_com -a input_file=pgim_com.jl -o pgim_all_data.csv`