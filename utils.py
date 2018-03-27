
def build_forward_backward_hash(unique_values):
    num_unique = len(unique_values)
    fmap = dict(zip(unique_values, range(num_unique)))
    bmap = dict(zip(range(num_unique), unique_values))
    return fmap, bmap
