from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import SKU,SPU,SPUSpecification,SpecificationOption,SKUSpecification,SKUImage,GoodsCategory,GoodsChannel,Brand,ChannelGroup


# class SKUAdmin(admin.ModelAdmin):


admin.site.register(SKU)
admin.site.register(SPU)
admin.site.register(SPUSpecification)
admin.site.register(SpecificationOption)
admin.site.register(SKUSpecification)
admin.site.register(SKUImage)
admin.site.register(GoodsCategory)
admin.site.register(GoodsChannel)
admin.site.register(Brand)
admin.site.register(ChannelGroup)