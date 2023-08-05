Changelog
*********

- 1.0.8 - 2021-06-18
    - review dependencies
    - licensing source code

- 1.0.7 - 2021-06-01
    - add `with_product_estimation` parameter for trades
    - documentation updates
    - availability to update the endpoints url for dev purpose

- 1.0.5 - 2021-02-24
    - add `withFreightView` param according to the documentation
    - add `withOrderbook` param according to the documentation
    - add Contracting metric for fleet-development series/vessels
    - add product and grade split for congestion series
    - add `Fleet Metrics` feature on LNG platform

- 1.0.4 - 2021-01-29
    - fix boolean fields always reflecting as `True` in pandas
    - continuous integration improvements

- 1.0.3 - 2021-01-13
    - change version requirement for a lib : `numpy>=1.19.0`
    - new versions notification through a log message on `Configuration` object creation
    - better error handling on authentication failure

- 1.0.2 - 2020-12-17
    - allow proxy configuration in `Configuration` object
    - allow usage of local ssl certificate in `Configuration` object
    - allow disabling of ssl verification (default set to False) in `Configuration` object

- 1.0.1 - 2020-12-09
    - module and classes names uniformization
    - fix usage of doc string

- 1.0.0 - 2020-12-09
    - first version
