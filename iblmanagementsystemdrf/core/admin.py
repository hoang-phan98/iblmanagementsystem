from django.contrib import admin
from core.models import Course, Interview, Supervisor, Student, Company, Placement, Unit, UnitCourse, Application

# Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     readonly_fields = ['id', 'slug']
# admin.site.register(Product, ProductAdmin)

admin.site.register(Course)
admin.site.register(Interview)
admin.site.register(Supervisor)
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Placement)
admin.site.register(Unit)
admin.site.register(UnitCourse)
admin.site.register(Application)
