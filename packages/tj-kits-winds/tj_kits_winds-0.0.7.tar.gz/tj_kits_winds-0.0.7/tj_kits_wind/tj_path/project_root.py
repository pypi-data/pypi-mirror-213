def get_project_root(project_name: str | None = None, defalut_path: str | None = "/tmp/JustDemo") -> str:
    if not project_name:
        return defalut_path

    try:
        frame = inspect.currentframe().f_back
        str_frame = str(frame)

        # [
        #   '<frame at 0x7fa4a58a1a40',
        #   " file '/.../PytestForDocker/main.py'",
        #   ' line 7',
        #   ' code <module>>'
        #   ]
        frame_split = str_frame.split(",")

        res = ""
        for ele in frame_split:
            ele = ele.replace(" ", "")
            if ele.startswith("file'"):
                ele = ele[4:]
                res = ele.replace("'", "")
                break

        if not res:
            return defalut_path

        a = res.find(project_name)
        if a == -1:
            return defalut_path
        else:
            return os.path.join(res[:a], project_name)
    except Exception:
        return defalut_path
