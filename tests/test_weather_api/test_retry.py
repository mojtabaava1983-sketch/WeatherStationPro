from weather_api.retry import RetryPolicy
def test_retry():
    s={"n":0}
    def op():
        s["n"]+=1
        if s["n"]<3: raise TimeoutError()
        return "ok"
    assert RetryPolicy(3,0).run(op, lambda e:isinstance(e,TimeoutError)) == ("ok",3)
