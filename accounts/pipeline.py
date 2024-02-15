from social_core.pipeline.user import create_user


def social_auth_create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {"user": user}

    user = create_user(strategy, details, backend, user=None, *args, **kwargs)

    return {"user": user}
