from django.db import models
#As of September 09, 2024 from https://www.ontario.ca/page/find-school-board-or-school-authority
school_boards = {
None: "------------",
"0" : "Algoma District School Board",
"1" : "Algonquin and Lakeshore Catholic District School Board",
"2" : "Avon Maitland District School Board",
"3" : "Bluewater District School Board",
"4" : "Brant Haldimand Norfolk Catholic District School Board",
"5" : "Bruce-Grey Catholic District School Board",
"6" : "CHEO School Authority",
"7" : "Catholic District School Board of Eastern Ontario",
"8" : "Conseil des écoles publiques de l'Est de l'Ontario",
"9" : "Conseil scolaire Viamonde",
"10" : "Conseil scolaire catholique MonAvenir",
"11" : "Conseil scolaire catholique Providence",
"12" : "Conseil scolaire de district catholique Franco-Nord",
"13" : "Conseil scolaire de district catholique de l'Est ontarien",
"14" : "Conseil scolaire de district catholique des Aurores boréales",
"15" : "Conseil scolaire de district catholique des Grandes Rivières",
"16" : "Conseil scolaire de district catholique du Centre-Est de l'Ontario",
"17" : "Conseil scolaire de district catholique du Nouvel-Ontario",
"18" : "Conseil scolaire public du Grand Nord de l'Ontario",
"19" : "Conseil scolaire public du Nord-Est de l'Ontario",
"20" : "Consortium Centre Jules-Léger",
"21" : "District School Board Ontario North East",
"22" : "District School Board of Niagara",
"23" : "Dufferin-Peel Catholic District School Board",
"24" : "Durham Catholic District School Board",
"25" : "Durham District School Board",
"26" : "Grand Erie District School Board",
"27" : "Grandview School Authority",
"28" : "Greater Essex County District School Board",
"29" : "Halton Catholic District School Board",
"30" : "Halton District School Board",
"31" : "Hamilton-Wentworth Catholic District School Board",
"32" : "Hamilton-Wentworth District School Board",
"33" : "Hastings & Prince Edward District School Board",
"34" : "Huron Perth Catholic District School Board",
"35" : "Huron-Superior Catholic District School Board",
"36" : "James Bay Lowlands Secondary School Board",
"37" : "John McGivney Children's Centre School Authority",
"38" : "Kawartha Pine Ridge District School Board",
"39" : "Keewatin-Patricia District School Board",
"40" : "Kenora Catholic District School Board",
"41" : "KidsAbility Education Authority",
"42" : "Lakehead District School Board",
"43" : "Lambton Kent District School Board",
"44" : "Limestone District School Board",
"45" : "London District Catholic School Board",
"46" : "Near North District School Board",
"47" : "Niagara Catholic District School Board",
"48" : "Niagara Peninsula Children's Centre School Authority",
"49" : "Nipissing-Parry Sound Catholic District School Board",
"50" : "Northwest Catholic District School Board",
"51" : "Ottawa Catholic School Board",
"52" : "Ottawa-Carleton District School Board",
"53" : "Peel District School Board",
"54" : "Peterborough Victoria Northumberland and Clarington Catholic District School Board",
"55" : "Provincial and Demonstration Schools",
"56" : "Rainbow District School Board",
"57" : "Rainy River District School Board",
"58" : "Renfrew County Catholic District School Board",
"59" : "Renfrew County District School Board",
"60" : "Simcoe County District School Board",
"61" : "Simcoe Muskoka Catholic District School Board",
"62" : "St Clair Catholic District School Board",
"63" : "Sudbury Catholic District School Board",
"64" : "Superior-Greenstone District School Board",
"65" : "Thames Valley District School Board",
"66" : "Thunder Bay Catholic District School Board",
"67" : "Toronto Catholic District School Board",
"68" : "Toronto District School Board",
"69" : "Trillium Lakelands District School Board",
"70" : "Upper Canada District School Board",
"71" : "Upper Grand District School Board",
"72" : "Waterloo Catholic District School Board",
"73" : "Waterloo Region District School Board",
"74" : "Wellington Catholic District School Board",
"75" : "Windsor-Essex Catholic District School Board",
"76" : "York Catholic District School Board",
"77" : "York Region District School Board"}

class Courses(models.Model):
    course_code = models.CharField(max_length=5)
    description = models.CharField(max_length=1023)
    course_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    prereq = models.CharField(max_length=1023)
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_code}"

    def grade(self):
        grade_chr = self.course_code[3]
        if grade_chr in "1234":
            return [9,10,11,12][["1","2","3","4"].index(grade_chr)]
        else:
            return 0

    def level(self):
        lvl_chr = self.course_code[4]
        if lvl_chr in "WPDUMCEO":
            return ["De-streamed","Applied","Academic","University","University/College","College","Workplace","Open"][["W","P","D","U","M","C","E","O"].index(lvl_chr)]
        else:
            return "<ERR, CODE NOT WPDUMCEO>"

class Reviews(models.Model):
    course_code = models.CharField(max_length=5)
    online = models.BooleanField()
    review_text = models.CharField(max_length=1023)
    interesting_rating = models.IntegerField()
    easy_rating = models.IntegerField()
    overall_rating = models.IntegerField()
    review_date = models.IntegerField()
    user_school_board = models.CharField(max_length=2,choices=school_boards)
    moderated = models.BooleanField()
    user_ip = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.course_code} review from {self.review_date}"
