import os
import json
import datetime
import time
file="tasks.json"
#if file doesnt exist create it
if not os.path.exists(file):
    with open(file,"w")as f:
        json.dump({},f)
    
# A Tasks class to handle all methods that work on an individual task
class Tasks:
    def __init__(self,title:str,priority:str,deadline:str,estimated_time:int,status:str):
        self.title=title
        self.priority=priority
        self.deadline=deadline
        self.et=estimated_time
        self.status=status
    @staticmethod
    #simple method to get current time
    def gettime():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    #method to convert the class variables into a dictionary
    def to_dict(self):
        t_dict={"Title" : self.title,"Priority": self.priority, "Deadline" : self.deadline, "Estimated_time" : self.et,"Status" : self.status}
        return t_dict
    @classmethod
    #method to create an object of a dictionary
    def from_dict(cls,t:dict):
        return cls(t["Title"],
                   t["Priority"],
                   t["Deadline"],
                   t["Estimated_time"],
                   t["Status"])
    #method to check if a task is overdue or not
    def is_overdue(self):
        deadline=datetime.datetime.strptime(self.deadline,"%Y-%m-%d %H:%M")
        time_now=datetime.datetime.strptime(Tasks.gettime(),"%Y-%m-%d %H:%M")
        if deadline<=time_now:
            return True
        else:
            return False
    #method to check how much time is remaining to finish a task
    def time_remaining(self):
        deadline=datetime.datetime.strptime(self.deadline,"%Y-%m-%d %H:%M")
        time_now=datetime.datetime.strptime(Tasks.gettime(),"%Y-%m-%d %H:%M")
        rem=deadline-time_now
        if rem.total_seconds()<=0:
            return "No Time Remaining!"
        days=rem.days
        hours=rem.seconds//3600
        minutes=(rem.seconds%3600)//60
        return f"{days}d , {hours}h , {minutes}m"
#task Manager class which handle all functions and calculations that require multiple tasks
class TaskManager:
    def __init__(self):
        #loading the tasks dictionary from a file
        with open(file,"r")as f:
            self.tasks=json.load(f)
        #variable to get id to assign ids to a task
        self.last_id=len(self.tasks)
    #method to get an id to assign to a task
    def reload_tasks(self):
        with open(file,"r")as f:
            self.tasks=json.load(f)
    def idgen(self):
        self.last_id+=1
        return str(self.last_id)
    #method to add a task by first making an object of the arguments then converting it to dictionary and storing it in a file
   
    def addtask(self,title:str,priority:str,deadline:str,estimated_time:int):
        task_id=self.idgen()
        t=Tasks(title,priority,deadline,estimated_time,"Pending")
        t_dict=t.to_dict()
        self.tasks[task_id]=t_dict
        self.save_tasks()
        print("Task Added Successfully✅")
    #method to remove task
    def remove_task(self,task_id:str):
        if task_id in self.tasks:
            c=input("Confirm to delete this task?(y/n)")
            if c[0].lower()=="y":
                del self.tasks[task_id]
                self.save_tasks()
                print("Task Removed Successfully✅")
        else:
            print("Invalid Task ID")
    #method to get a task by its id
    def get_task(self,task_id:str):
        if task_id in self.tasks:
            print("---------------------------")
            for key,value in self.tasks[task_id].items():
                print(f"{key} : {value}")
            print("---------------------------")
        else:
            print("Invalid Task ID")
    #method to get all pending tasks, if no pending tasks then print all tasks completed
    def get_pending_tasks(self):
        found=False
        for task in self.tasks:
            if self.tasks[task]["Status"]=="Pending":
                found=True
                print(f"----------#{task}-----------")
                for key,value in self.tasks[task].items():
                    print(f"{key} : {value}")
        if not found:
            print("All Tasks Are Completed")
    #method to get all completed tasks
    def get_completed_tasks(self):
        found=False
        for task in self.tasks:
            if self.tasks[task]["Status"]=="Completed":
                found=True
                print(f"----------#{task}-----------")
                for key,value in self.tasks[task].items():
                    print(f"{key} : {value}")
        if not found:
            print("All Tasks Are Pending")
    #method to mark a task completed by its id
    def mark_completed(self,task_id:str):
        if task_id in self.tasks:
            self.tasks[task_id]["Status"]="Completed"
            self.save_tasks()
            print("Task Marked Completed  Successfully✅")
        else:
            print("Invlaid Task Id")
    #method to save a task to a file
    def save_tasks(self):
        with open(file,"w")as f:
            json.dump(self.tasks,f,indent=4,sort_keys=True)
    #############################################
    """These two methods are also present in the Tasks class and are being functioned from the Tasks class itself since they cant be called directly they are being called using a function"""
    #method to check if a task is overdue
    def is_overdue(self,task_id:str):
        if task_id in self.tasks:
            t_ob=Tasks.from_dict(self.tasks[task_id])
            if t_ob.is_overdue():
                print("The Task Is Overdue")
            else:
                print("The Task Is Not Overdue")
        else:
            print("Invalid Task Id")
    #method to get the time remaining to complete a task
    def get_time_remaining(self,task_id:str):
        if task_id in self.tasks:
            t_ob=Tasks.from_dict(self.tasks[task_id])
            print(t_ob.time_remaining())
        else:
            print("Invalid Task Id")
    #########################################
    #function to mark all tasks which are overdue
    def mark_overdue_task(self):
        for task_id in self.tasks:
            t_ob=Tasks.from_dict(self.tasks[task_id])
            if t_ob.is_overdue() and t_ob.status=="Pending":
                self.tasks[task_id]["Status"]="Overdue"
        print("Overdue Tasks Marked Successfully✅")
        self.save_tasks()
#this class does operations like sorting and operations related to deadline and urgency of a task
class PriorityEngine:
    #initializing a task dictionary by creating object of the taskmanager class
    def __init__(self):
        t=TaskManager()
        t.reload_tasks()
        self.tasks=t.tasks
        
        #it sets a priority list to be used to sort tasks
        self.priority={"High":3,"Medium":2,"Low":1}
    @staticmethod
    #method used to display a dictionary
    def display(d:dict):
        for key,value in d.items():
            print(f"{key} : {value}")
    #method to sort task based on their deadlines or priority
    def sort_tasks(self):
        ch=input("Sort on the basis or deadline or priority?(d=deadline/p=priority)")
        if ch.lower().strip()=="d":
            sorted_ids=sorted(self.tasks,key=lambda task_id:datetime.datetime.strptime(self.tasks[task_id]["Deadline"],"%Y-%m-%d %H:%M"))
            for task_id in sorted_ids:
                if self.tasks[task_id]["Status"]!="Completed":
                        print(f"-------#{task_id}-------")
                        PriorityEngine.display(self.tasks[task_id])
        elif ch.lower().strip()=="p":
            sorted_ids=sorted(self.tasks,key=lambda task_id: self.priority[self.tasks[task_id]["Priority"]])
            for task_id in sorted_ids:
                if self.tasks[task_id]["Status"]!="Completed":
                    print(f"--------#{task_id}--------")
                    PriorityEngine.display(self.tasks[task_id])
        else:
            print("Invalid Input!")
    #method to get urgent tasks. This first filters all tasks which are not completed and their priority is High and then it sorts tasks based on their deadline then prints them
    def get_urgent_tasks(self):
        urgent={k:v for k,v in self.tasks.items() if self.tasks[k]["Status"]!="Completed" and self.tasks[k]["Priority"]=="High"}
        urgent=sorted(urgent,key=lambda task_id: datetime.datetime.strptime(urgent[task_id]["Deadline"],"%Y-%m-%d %H:%M")) 
        for task_id in urgent:
            print(f"-------#{task_id}-------")
            PriorityEngine.display(self.tasks[task_id])
class DailyPlanner:
    def __init__(self):
        t=TaskManager()
        t.reload_tasks()
        self.tasks=t.tasks
    def generate_plan(self,available_time):
        plan={k:v for k,v in self.tasks.items() if self.tasks[k]["Status"]!="Completed"}
        sorted_id=sorted(plan,key=lambda task_id: datetime.datetime.strptime(plan[task_id]["Deadline"],"%Y-%m-%d %H:%M"))
        today_plan={}
        overflow={}
        remaining_time=available_time
        for ids in sorted_id:
            estimated_time=self.tasks[ids]["Estimated_time"]
            if estimated_time<=remaining_time:
                today_plan[ids]=self.tasks[ids]
                remaining_time-=self.tasks[ids]["Estimated_time"]
            else:
                overflow[ids]=self.tasks[ids]
        return [today_plan,overflow,remaining_time]
        
        

    def suggest_breaks(self):
        planned_time=0
        for value in self.tasks.values():
            if value["Status"]!="Completed":
                planned_time+=value["Estimated_time"]
        print("\n🕒 Break Suggestions")

        if planned_time <= 120:
            print("• No formal breaks needed. Just stay hydrated ☕")

        elif planned_time <= 240:
            print("• Take a 5-10 min break after every 1 hour")

        elif planned_time <= 360:
            print("• Take a 10-15 min break after every 90 minutes")
            print("• One longer break (20 min) midway")

        else:
            print("• You’re planning a long day ⚠️")
            print("• Take a 10 min break every hour")
            print("• Take a long break (30–45 min) after 4 hours")
        
    def warn_overload(self,available_time):
        total_time=0
        for keys in self.tasks:
            total_time+=self.tasks[keys]["Estimated_time"]
        if total_time>available_time:
            print(f"You are overloaded by {total_time-available_time}m")
class Menu:
    def show_main_menu(self):
        while True:
            print("===============================")
            print(f"{'Task System'.center(31)}")
            print("===============================")
            ch=int(input("1.Task Manager\n2.Task Insights\n3.Planning & Productivity\n4.System Utilities\n5.Exit: "))
            if ch==1:
                self.task_management()
            elif ch==2:
                self.task_insights()
            elif ch==3:
                self.planning_and_productivity()
            elif ch==4:
                self.system_utilities()
            elif ch==5:
                return
            else:
                    print("Invalid Input!")
    def task_management(self):
        
        tasks=TaskManager()
        while True:
            print("===============================")
            print(f"{'Task Manager'.center(31)}")
            print("===============================")
            ch=int(input("1.Add Task\n2.Remove Task\n3.View Task By ID\n4.View Pending Tasks\n5.View Completed Tasks\n6.Mark Task as Completed\n7.Back To Main Menu: "))
            if ch==1:
                title=input("Enter The Title Of The Task: ")
                priority=input("Enter The Priority Of The Task('High'/'Medium'/'Low'): ")
                if priority=="High" or priority=="Medium" or priority=="Low":
                    
                    deadline=input("Enter The Deadline Of The Task(YYYY-MM-DD hh:mm)")
                    try:
                        datetime.datetime.strptime(deadline,"%Y-%m-%d %H:%M")
                    except:
                        print("Invalid Deadline")
                        print("Deadline Example: ",Tasks.gettime())
                    estimated_time=int(input("Enter The Estimated Time In Minutes: "))
                    tasks.addtask(title,priority,deadline,estimated_time)
                    
                else:
                    print("Invalid Priority Value")
            elif ch==2:
                task_id=input("Enter The Task Id: ")
                tasks.remove_task(task_id)
                
            elif ch==3:
                task_id=input("Enter The Task Id: ")
                tasks.get_task(task_id)
                
            elif ch==4:
                tasks.get_pending_tasks()
                
            elif ch==5:
                tasks.get_completed_tasks()
                
            elif ch==6:
                task_id=input("Enter The Task Id: ")
                tasks.mark_completed(task_id)
                
            elif ch==7:
                return
            else:
                print("Invalid Input!")
    def task_insights(self):
        tasks=TaskManager()
        while True:
            print("===============================")
            print(f"{'Task Insights'.center(31)}")
            print("===============================")
            ch=int(input("1.Check If Task Is Overdue\n2.Get Time Remaining For A Task\n3.Mark All Overdue Tasks\n4.Back To Main Menu: "))
            if ch==1:
                task_id=input("Enter the task Id: ")
                tasks.is_overdue(task_id)
                
            elif ch==2:
                task_id=input("Enter the task Id: ")
                tasks.get_time_remaining(task_id)
                
            elif ch==3:
                tasks.mark_overdue_task()
                
            elif ch==4:
                return
            else:
                print("Invalid Input!")
    def planning_and_productivity(self):
        
        priority=PriorityEngine()
        planning=DailyPlanner()
        
        while True:
            print("===============================")
            print(f"{'Planning and Productivity'.center(31)}")
            print("===============================")
            ch=int(input("1.Sort Tasks\n2.Show Urgent Tasks\n3.Generate Daily Plan\n4.Back To Main Menu: "))
            if ch==1:
                priority.sort_tasks()
                
            elif ch==2:
                priority.get_urgent_tasks()
                
            elif ch==3:
                time=int(input("Enter your available time in minutes: "))
                details=planning.generate_plan(time)
                print("-----------Today's Plan-------------")
                if details[0]:
                    for tasks in details[0]:
                        print(f"----------#{tasks}------------")
                        PriorityEngine.display(details[0][tasks])
                    print("-----------Extra tasks--------------")
                    if details[1]:
                        for tasks in details[1]:
                            print(f"----------#{tasks}------------")
                            PriorityEngine.display(details[1][tasks])
                    else:
                        print("No Extra Tasks")
                    print("------------Extra Time Left-------- ")
                    if details[2]:
                        print(f"{details[2]}m")
                    else:
                        print("No Extra Time Left")
                    planning.suggest_breaks()
                    planning.warn_overload(time)
                    
                else:
                    print("No Tasks In Today's Plan")
            elif ch==4:
                return
            else:
                print("Invalid choice!")
    def system_utilities(self):
        
        while True:
            print("===============================")
            print(f"{'System Utilities'.center(31)}")
            print("===============================")
            ch=int(input("1.Clear Screen\n2.Reload Tasks From File\n3.Back To Main Menu: "))
            if ch==1:
                os.system("cls") if os.name=="nt" else os.system("clear")
                
            if ch==2:
                print("Task Reloaded On Next Operation✅")
                
            elif ch==3:
                return
            else:
                print("Invalid Choice!")
    
        
if __name__=="__main__":
    obj=Menu()
    obj.show_main_menu()



