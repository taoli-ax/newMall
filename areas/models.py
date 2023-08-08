from django.db import models


# Create your models here.
class Area(models.Model):
    """
    area_set.all()反向查询
    A 1- B 多
    A.B_set 查询关联A的所有B
    A.related_name 等效于 A.B_set
    """
    name = models.CharField(max_length=20, verbose_name='Province Name')
    parent = models.ForeignKey('self',
                               on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True,
                               blank=True,
                               verbose_name='up administration'
                               )
    class Meta:
        db_table='tb_areas'
        verbose_name='省市区'

    def __str__(self):
        return self.name


