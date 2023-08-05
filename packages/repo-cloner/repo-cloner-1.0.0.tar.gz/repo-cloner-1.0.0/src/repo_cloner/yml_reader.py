import yaml


def read_repos_list(path_to_yaml):
    with open(path_to_yaml) as file:
        try:
            doc = yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print("Error in the file: {}, error: {}".format(path_to_yaml, exc))
            return []
        return doc
        # if isinstance(doc, list):
        #     return doc
        # print("Only list of repos in the .yml files are already supported, returning empty list")
        # return []
