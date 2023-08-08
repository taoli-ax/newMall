from django.db import models


# Create your models here.
class ChannelGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name="channel")

    class Meta:
        db_table = "tb_channel_group"

    def __str__(self):
        return self.name


class GoodsCategory(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="subs")

    class Meta:
        db_table = "tb_goods_category"

    def __str__(self):
        return self.name


class GoodsChannel(models.Model):
    ChannelGroup = models.ForeignKey(
        ChannelGroup,
        on_delete=models.PROTECT,
        related_name="goods_channel",
        verbose_name="channel_group"
    )
    category = models.ForeignKey(
        GoodsCategory,
        on_delete=models.PROTECT,
        related_name="category_goods_channel",
        verbose_name="channel_category"
    )
    url = models.URLField(verbose_name="channel_url")
    sequence = models.IntegerField(verbose_name="goods_sequence")

    class Meta:
        db_table = "tb_goods_channel"

    def __str__(self):
        return self.ChannelGroup.name + " " + self.category.name


class Brand(models.Model):
    """品牌"""
    name = models.CharField(max_length=100, verbose_name="brand")
    logo = models.ImageField(verbose_name="logo_link")
    first_letter = models.CharField(max_length=1, verbose_name="brandFirstLetter")

    class Meta:
        db_table = "tb_brand"

    def __str__(self):
        return self.name


class SPU(models.Model):
    """ 标准商品单元 系列"""
    name = models.CharField(max_length=100, verbose_name="product")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brand",verbose_name="brand_id")
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name="category1",
                                  verbose_name="category1_id")
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name="category2",
                                  verbose_name="category2_id")
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name="category3",
                                  verbose_name="category3_id")
    sales = models.IntegerField(default=0, verbose_name="sales")
    comments = models.IntegerField(default=0, verbose_name="comments")
    desc_detail = models.TextField(default='', verbose_name="detail")
    desc_pack = models.TextField(default='', verbose_name="packInfo")
    desc_service = models.TextField(default='', verbose_name="after_sales")

    class Meta:
        db_table = "tb_spu"

    def __str__(self):
        return self.name


class SKU(models.Model):
    """ 库存保有单元 """
    name = models.CharField(max_length=100, verbose_name="sku_name")
    caption = models.CharField(max_length=500, verbose_name="caption")
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE,related_name="spu", verbose_name="spu_id")
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name="category",
                                 verbose_name="category_id")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="costPrice")
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="marketPrice")
    stock = models.IntegerField(default=0, verbose_name="stock")
    sales = models.IntegerField(default=0, verbose_name="sales")
    comments = models.IntegerField(default=0, verbose_name="comments")
    is_launched = models.BooleanField(default=True, verbose_name="isLaunched")
    default_image_url = models.URLField(default='', null=True, blank=True, verbose_name="DefaultImageUrl")

    class Meta:
        db_table = "tb_sku"

    def __str__(self):
        return self.name


class SPUSpecification(models.Model):
    """ 规格详情 """
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name="specs", verbose_name="spu_id")
    name = models.CharField(max_length=100, verbose_name="spu")

    class Meta:
        db_table = "tb_spu_specification"

    def __str__(self):
        return self.name


class SpecificationOption(models.Model):
    """ 规格选项 """
    spec = models.ForeignKey(SPUSpecification, verbose_name="spec_id", related_name="options", on_delete=models.CASCADE)
    value = models.CharField(max_length=300, verbose_name="optionValue")

    class Meta:
        db_table = "tb_specification_option"

    def __str__(self):
        return self.spec.name


class SKUSpecification(models.Model):
    """
    商品具体规格
    """
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, related_name="sku", verbose_name="sku_id")
    spec = models.ForeignKey(SPUSpecification, on_delete=models.PROTECT, related_name="SPUSpecification",
                             verbose_name="spec_id")
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, related_name="SpecificationOption",
                               verbose_name="option_id")

    class Meta:
        db_table = "tb_sku_specification"

    def __str__(self):
        return self.sku.name + " : " + self.spec.name + "-" + self.option.value


class SKUImage(models.Model):
    """ SKU图片 """
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, related_name="image_sku", verbose_name="sku_id")
    image = models.ImageField(verbose_name="imageUrl")

    class Meta:
        db_table = "tb_sku_image"

    def __str__(self):
        return self.sku.name + " " + self.id
