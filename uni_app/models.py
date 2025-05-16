from django.db import models

# Create your models here.


class Semester(models.Model):
    """
    Repräsentiert ein akademisches Semester.

    Felder:
    - name: Der Name des Semesters.
    """
    name = models.CharField(max_length=100)  # z. B. "Sommersemester 2025"

    def __str__(self):
        return self.name


class Professor(models.Model):
    """
    Repräsentiert einen Professor, der Kurse unterrichtet.

    Felder:
    - first_name: Vorname des Professors.
    - last_name: Nachname des Professors.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    """
    Repräsentiert einen Kurs, der von einem Professor unterrichtet und in einem bestimmten
    Semester angeboten wird.

    Felder:
    - name: Der Name des Kurses.
    - description: Eine textuelle Beschreibung des Kurses.
    - semester: Das Semester, in dem der Kurs stattfindet.
    - professor: Der Professor, der den Kurs unterrichtet.
        - on_delete=models.SET_NULL: Wenn der Professor gelöscht wird, wird der Wert im Feld
          professor auf NULL gesetzt (also kein Professor mehr zugeordnet).
            - null=True: Erlaubt NULL-Werte in der Datenbank.
            - blank=True: Erlaubt leere Eingaben in Forms oder im Admin.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="courses")
    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses"
    )

    def __str__(self):
        return self.name


class CourseDescription(models.Model):
    """
    Repräsentiert eine ausführliche Beschreibung für einen bestimmten Kurs.

    Felder:
    - course: Der Kurs, zu dem die Beschreibung gehört (1:1-Beziehung).
    - description: Der eigentliche Beschreibungstext.
    """
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Beschreibung zu {self.course.name}"


class Student(models.Model):
    """
    Repräsentiert einen Studierenden, der mehrere Kurse besuchen kann.

    Felder:
    - first_name: Vorname des Studenten.
    - last_name: Nachname des Studenten.
    - contact_info: Kontaktinformationen (optional).
    - courses: Kurse, an denen der Student teilnimmt (viele-zu-viele).
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact_info = models.TextField(max_length=300, blank=True, default="")
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentIDCard(models.Model):
    """
    Repräsentiert einen Studentenausweis, der einem einzelnen Studenten zugeordnet ist.

    Felder:
    - has_card: Gibt an, ob ein Student einen Ausweis besitzt.
    - student: Der zugehörige Student (1:1-Beziehung).
    """
    has_card = models.BooleanField(default=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ausweis von {self.student}"
