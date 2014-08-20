def full_name(image, registry=None, tag=None):
    if registry:
        image = '{}/{}'.format(registry, image)
    if tag:
        image = '{}:{}'.format(image, tag)

    return image
