
import copy

MISC_CATEGORY_LABEL = "-- Misc --"

class HardwareSet(object):
    """A class to manage the categorized instance types.
    
    It takes flat instance types array and builds a nested structure where instance types exist in
    categories.
    """

    def __init__(self, instance_types):
        self.instance_types = self.build_unique(instance_types)
        self.categories = self.build_categories()
        
    @staticmethod
    def build_unique(instance_types):
        """Build a dictionary of instance types using name as key.
        
        Remove any instance types whose description has already been seen. We can't have duplicate
        descriptions.
        """
        result = {}
        seen_descriptions = set() 
        for it in instance_types:
            if it["description"] in seen_descriptions:
                continue
            result[it["name"]] = it
            seen_descriptions.add(it["description"])
        return result
    
    
    def build_categories(self):
        """Build a sorted list of categories, each category containing a sorted list of machines"""
 
        dikt = {}
        for key in self.instance_types:
            it = self.instance_types[key]
            categories = it.get("categories") or []
            if not categories:
                categories.append({"label": MISC_CATEGORY_LABEL, "order": 999})
            for category in categories:
                label = category["label"]
                if label not in dikt:
                    dikt[label] = {"label": label, "content": [], "order": category["order"]}
                dikt[label]["content"].append(it)

        result = []
        for label in dikt:
            category = dikt[label]
            category["content"].sort(key=lambda k: (k["cores"], k["memory"]))
            result.append(category)
        return sorted(result, key=lambda k: k["order"])
 
 
    def get_model(self, with_misc=False):
        """Returns the categories structure with filtering and renaming ready for some UI.

        with_misc: Include misc category. The misc category is always included if it's the only one.
        """
        result = []
        should_remove_misc = not with_misc and len( self.categories) > 1

        for category in self.categories:
            if should_remove_misc and category["label"] == MISC_CATEGORY_LABEL:
                continue

            result.append({
                "label": category["label"],
                "content": list(map(lambda k: {"label": k["description"], "value": k["name"]} , category["content"]))
            })

        return result
   
    def find(self, name):
        return self.instance_types.get(name)
    
    def number_of_categories(self):
        return len(self.categories)
    