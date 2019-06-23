from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

premium_search_args = load_credentials(filename="tweet_creds.yaml",
    yaml_key="search_tweets_api",
    env_overwrite=False)

rule = gen_rule_payload("from:jack",
                        from_date="2017-09-01", #UTC 2017-09-01 00:00
                        to_date="2017-10-30",#UTC 2017-10-30 00:00
                        results_per_call=100)
print(rule)

tweets = collect_results(rule, max_results=100, result_stream_args=premium_search_args)