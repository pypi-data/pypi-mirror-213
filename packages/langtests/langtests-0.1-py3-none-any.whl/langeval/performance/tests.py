from langeval.performance.rouge import RougeTest


def test(method, **kwargs):
    df = kwargs.pop('df', None)
    rouge_examples = ['rouge1', 'rougeL']

    if method in rouge_examples:
        tester = RougeTest()
        result_df = tester.apply(method, df, **kwargs)
    else:
        raise ValueError(f"Unknown method: {method}")

    return result_df
