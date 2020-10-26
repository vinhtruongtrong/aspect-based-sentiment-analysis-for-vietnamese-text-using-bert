import re
class BaseMethod(object):
    def __init__(self, domain):
        if(domain == 'restaurant'):
            self.aspect_categories = {
                'FOOD#STYLE&OPTIONS': 'phong_cách đồ_ăn', 
                'FOOD#QUALITY': 'chất_lượng đồ_ăn', 
                'AMBIENCE#GENERAL' : 'cảnh_quan',
                'RESTAURANT#GENERAL' : 'tổng_thể', 
                'SERVICE#GENERAL' : 'dịch_vụ', 
                'FOOD#PRICES' : 'giá thức_ăn',
                'RESTAURANT#PRICES' : 'giá tổng_thể', 
                'LOCATION#GENERAL' : 'vị_trí', 
                'RESTAURANT#MISCELLANEOUS' : 'khác',
                'DRINKS#STYLE&OPTIONS' : 'phong_cách nước', 
                'DRINKS#PRICES' : 'giá nước', 
                'DRINKS#QUALITY' : 'chất_lượng nước'
                }
        else:
            self.aspect_categories = {
                'FACILITIES#DESIGN&FEATURES' : 'thiết_kế cơ_sở vật_chất', 
                'SERVICE#GENERAL' : 'dịch_vụ', 
                'LOCATION#GENERAL':'vị_trí',
                'HOTEL#DESIGN&FEATURES':'thiết_kế khách_sạn', 
                'HOTEL#COMFORT':'tiện_nghi khách_sạn', 
                'ROOMS#DESIGN&FEATURES':'thiết_kế phòng',
                'ROOM_AMENITIES#QUALITY':'chất_lượng nhà_vệ_sinh', 
                'ROOM_AMENITIES#CLEANLINESS':'mức_độ sạch_sẽ nhà_vệ_sinh', 
                'HOTEL#GENERAL':'tổng_quan khách sạn',
                'FACILITIES#COMFORT':'hài_lòng tiện_nghi', 
                'FACILITIES#QUALITY':'chất_lượng cơ_sở vật_chất', 
                'DRINKS#QUALITY':'chất_lượng nước giải_khát',
                'ROOM_AMENITIES#DESIGN&FEATURES':'thiết_kế nhà_vệ_sinh',
                'ROOM_AMENITIES#COMFORT':'mức_độ hài_lòng nhà_vệ_sinh',
                'ROOMS#CLEANLINESS':'mức_độ sạch_sẽ phòng', 
                'HOTEL#CLEANLINESS':'mức_độ sạch_sẽ khách sạn', 
                'ROOMS#COMFORT':'tiện_nghi phòng',
                'FACILITIES#GENERAL':'cơ_sở vật_chất', 
                'DRINKS#STYLE&OPTIONS':'phong_cách nước giải_khát', 
                'ROOMS#GENERAL':'khách_sạn',
                'HOTEL#PRICES':'giá', 
                'HOTEL#QUALITY':'chất_lượng khách_sạn',
                'HOTEL#MISCELLANEOUS':'mặt_khác',
                'ROOM_AMENITIES#GENERAL':'nhà_vệ_sinh',
                'FACILITIES#PRICES':'giá tiện_nghị', 
                'ROOMS#PRICES':'giá phòng',
                'FACILITIES#CLEANLINESS':'mức_độ sạch_sẽ cơ_sở vật_chất',
                'FACILITIES#MISCELLANEOUS':'mặt_khác tiện_nghi',
                'DRINKS#MISCELLANEOUS':'mặt_khác nước giải_khát', 
                'ROOMS#MISCELLANEOUS':'mặt_khác phòng', 
                'DRINKS#PRICES':'giá nước giải_khát',
                'ROOMS#QUALITY':'chất_lượng phòng', 
                'ROOM_AMENITIES#MISCELLANEOUS':'mặt_khác tiện_nghi nhà_vệ_sinh',
                'ROOM_AMENITIES#PRICES':'giá tiện_nghi nhà_vệ_sinh'
            }
        self.labels_categories = {
                'positive' : 'tích_cực',
                'negative': 'tiêu_cực',
                'neutral' : 'trung_lập',
                'none' : 'không_có'
            }

    def get_labels(self, val):
        result = []
        aspects = re.findall(r'[\w#&]+', val)
        for i in range(0, len(aspects), 2):
            result.append([aspects[i], aspects[i+1]])
        return result

    def generate_data_frame(self, dataframe):
        raise NotImplementedError("generate_data_frame has be not implemented")