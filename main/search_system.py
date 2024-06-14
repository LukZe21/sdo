def search_query(query, discount_elements, event_elements):
    words = query.split(" ")
    score_dict = {}
    for idx, parent_element in enumerate([discount_elements, event_elements]):
        try:
            print(idx, parent_element)
            elements = parent_element[idx].query.all()
            for element in elements:
                # idx == 0 - Discount Elements; idx == 1 - Event Elements
                if idx == 0:
                    id = 'discount/' + str(element.id)
                elif idx == 1:
                    id = 'event/' + str(element.id)
                values_list = []

                name = element.name
                if idx == 0:
                    condition = element.condition
                elif idx == 1:
                    event_hoster = element.event_hoster
                    location = element.location

                description = element.description
                categories = element.categories

                if idx == 0:
                    for val in [name, condition, description, categories]:
                        values_list.append(val.split(" "))

                elif idx == 1:
                    for val in [name, condition, description, categories, event_hoster, location]:
                        values_list.append(val.split(" "))

                for values in values_list:
                    for value in values:
                        if value in words:
                            if id in score_dict.keys():
                                print(id)
                                score_dict[id] += 1
                            else:
                                score_dict[id] = 1
        except:
            continue

    return score_dict
