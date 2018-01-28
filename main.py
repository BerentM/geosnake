import alchemia

DB = alchemia.Database()

#DB.insertSource(post_code='14-260', city='Lubawa', street='Matejki',
#        house_number='29')

DB.calculateDistance(post_code='14-260', city='Lubawa', street='Matejki',
        house_number='29',destination_name='Katedra Wawelska')

