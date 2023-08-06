from rouge_score import rouge_scorer


class RougeTest:

    def __init__(self):
        pass

    @staticmethod
    def rouge_score(rouge_type, sentence_1, sentence_2):
        scorer = rouge_scorer.RougeScorer([rouge_type], use_stemmer=True)
        scores = scorer.score(sentence_1, sentence_2)
        return scores[rouge_type].fmeasure

    def apply(self, method, df, **kwargs):

        rouge_type = method
        output_col = kwargs['output_col']
        ideal_col = kwargs['ideal_col']

        df[rouge_type] = df.apply(lambda row: self.rouge_score(
            rouge_type, row[output_col], row[ideal_col]), axis=1
                 )
        return df
