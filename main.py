# we are going to use JSON= java script object notion
import json 
from abc import ABC , abstractmethod #abstract class
from pathlib import Path

Database="School_data.json"
data={"STUDENTS":[],"TEACHERS":[]}

if Path(Database).exists():
    with open(Database,'r') as f:
        content=f.read()
        if content:
            data=json.loads(content)

def save():
    with open(Database,'w') as f:
        json.dump(data,f,indent=4)

class Humans(ABC):

    @abstractmethod
    def getroles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def showdetails(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and  ".com" in email :
            return "vertified"
        else :
            return "CHECK YOUR EMAIL ONCE AGAIN"

    @staticmethod
    def check_mobile__no(mobile_no):
        if len==10 in mobile_no:
            return "Valid number"
        else:
            return "Inalid number"
        
class Students(Humans):
    def getroles(self):
        return "STUDENT"

    def register(self):
        name = input("Tell your Name:-")
        age = int(input("Tell your age:-"))
        Std = int(input("In which standard you are studying(ENTER NUMBER):-"))
        roll_no = int(input("Enter your roll no.:-"))
        email = input("Enter your or your parents email address:-")
        mobile_no = int(input("Enter your or your parent's mobile no:-"))

        if not Humans.validate_email(email): #check yt video once
            print("invalid!!!!")
            return
        if not Humans.check_mobile__no(mobile_no): #check yt video once
            print("invalid!!!!")
            return
        for i in data["STUDENTS"]:
            if i["name"]==name:
                print("THIS STUDENT IS ALREADY REGISTERED")
                return
        data["STUDENTS"].append({
            "name": name,
            "Std" : Std,
            "age" : age,
            "roll_no" : roll_no,
            "email":email,
            "mobile_no":mobile_no,
            'grades':{}
        })
    print(f"STUDENT{__name__} IS REGISTERED")
    save()
    def showdetails(self):
          name=input("Enter the name:-")
          for s in data["STUDENTS"]:
                 if s["name"]==name:
                       grades = s['grades']
                       avg = sum(grades.values()) / len(grades) if grades else 0

                       print(f"\n  NAME    : {s['name']}")
                       print(f"  STANDARD : {s['std']}")
                       print(f"  ROLL NO : {s['roll_no']}")
                       print(f"  GRADES : {grades}")
                       print(f"  AVERAGE : {avg:.1f}")
                       return
                 else:
                       print("STUDENT NOT FOUND")
                
                
                    

    def add_grades(self):
          name=input("Tell me the name:-")
          subject=input("Which subject:-")
          marks=float(input("Enter marks:-"))

          for i in data["STUDENTS"]:
                if i["name"]==name:
                      i["grades"][subject]=marks
                      save()
                      print("GRADES ADDED SUCCESSFULLY")
                      return
                else:
                      print("STUDENT NOT FOUND")
                


class Teachers(Humans):
     def getroles(self):
          return "TEACHER"

     def register(self):
          name = input("Tell your Name:-")
          age = int(input("Tell your age:-"))
          edu = input("Enter Education qualification in one line:-")
          subject=input("Enter which subject you teach:-")
          email = input("Enter your email address:-")
          mobile_no = int(input("Enter your mobile no:-"))
          
          if not Humans.validate_email(email): #check yt video once
                      print("invalid!!!!")
                      return
          if not Humans.check_mobile__no(mobile_no): #check yt video once
                      print("invalid!!!!")
                      return
          for i in data["TEACHERS"]:
                      if i["name"]==name:
                          print("THIS TEACHER IS ALREADY REGISTERED")
                          return
          data["TEACHERS"].append({
                      "name": name,
                      "age" : age,
                      "edu" : edu,
                      "subject" : subject,
                      "email":email,
                      "mobile_no":mobile_no,
          })
          save()
     print(f"TEACHER{__name__} IS REGISTERED")
     def showdetails(self):
               name=input("Enter the name:-")
               for s in data["TEACHERS"]:
                      if s["name"]==name:                         
                            print(f"\n  NAME   : {s['name']}")
                            print(f"\n  AGE    : {s['age']}")
                            print(f"  EDUCATION : {s['edu']}")
                            print(f"  MOBILE NUMBER : {s['mobile_no']}")
                            print(f"  EMAIL  : {s['email']}")
                            print(f"  SUBJECT : {s['subject']}")
                            return
                      else:
                            print("TEACHER NOT FOUND")
          
          

stud = Students()
tech = Teachers()

print("PRESS 1 TO REGISTER AS A STUDENT!!")
print("PRESS 2 TO REGISTER AS A TEACHER!!")
print("PRESS 3 TO SEE TEACHER DETAILS")
print("PRESS 4 TO SEE STUDENT DETAILS")
print("PRESS 5 TO ENTER GRADES OF REGISTERED STUDENTS")

number=int(input("PLEASE ENTER YOUR NUMBER HERE:-"))

if number==1:
    stud.register()

elif number==2:
      tech.register()

elif number==3:
     tech.showdetails()

elif number==4:
      stud.showdetails()

elif number==5:
      stud.add_grades()
     