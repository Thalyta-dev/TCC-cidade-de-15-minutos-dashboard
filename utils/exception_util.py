class ExceptionUtil:

    @staticmethod
    def montar_erro_patronizado(exception: type[Exception]) -> str:
        return f"{type(exception).__name__} na linha {exception.__traceback__.tb_lineno} do arquivo {exception.__traceback__.tb_frame.f_code.co_filename}: {exception}"