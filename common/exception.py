class BizException(Exception):
    def __init__(self, msg):
        super(BizException, self).__init__(msg)
