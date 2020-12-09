from django.contrib import messages


def check_availability_in_session(self):
    is_order_id_equals = self.request.session.get('order', False) == self.get_object().id
    is_user_id_equals = check_ownership(self, is_order_id_equals)

    if not is_order_id_equals:
        add_page_not_exist_message(self.request)

    return is_order_id_equals and is_user_id_equals


def check_ownership(self, session_check=None):
    is_user_id_equals = self.request.user.id == self.get_object().buyer.id

    if not is_user_id_equals and (session_check is None or session_check):
        add_no_access_perm_message(self.request)
    return is_user_id_equals


def add_no_access_perm_message(rq):
    messages.add_message(
        rq,
        messages.ERROR,
        'You\'re not allowed to view this page.'
    )


def add_page_not_exist_message(rq):
    print('.')
    messages.add_message(
        rq,
        messages.INFO,
        'Requested checkout page is no longer exist.'
    )
