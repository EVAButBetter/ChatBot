import argparse
from ai_intent.Professor import Professor

#
# for testing, useless
#


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=False, type=str, default="get_slot")
    parser.add_argument("--intent", required=False, type=str, default="Professor")
    opt = parser.parse_args()

    cls = globals()[opt.intent]()
    func = getattr(cls, opt.method)
    res = func()
    print(type(res))
    print(res)
