class Database:

    def __init__(self, session) -> None:
        self.session = session

    def update(self, data) -> None:
        session = self.session
        if data is not None:
            session.db.update(data, session.login['idToken'])

    def update_batch(self, path, input, index) -> None:

        if input is []:
            return

        session = self.session
        data: dict = {}

        for i, value in enumerate(input, index):
            value["id_list"] = i
            data[f"{path}/{value['id']}"] = value

        session.db.update(data)

    def get(self, path) -> tuple:
        session = self.session
        result = session.db.child(path).get(session.login['idToken']).val()
        return tuple(dict(result).values())

    def equal(self, path, param, equal_to) -> tuple:

        session = self.session
        result = session.db.child(path).order_by_child(param).equal_to(
            equal_to).get(session.login['idToken']).val()

        return tuple(dict(result).values())

    def between(self, path, param, start, end) -> tuple:

        session = self.session
        result = session.db.child(path).order_by_child(param).start_at(
            start).end_at(end).get(session.login['idToken']).val()

        return tuple(dict(result).values())

    def max(self, path, param) -> tuple:

        session = self.session
        result = session.db.child(path).order_by_child(param).limit_to_last(
            1).get(self.login['idToken']).val()

        return tuple(dict(result).values())
