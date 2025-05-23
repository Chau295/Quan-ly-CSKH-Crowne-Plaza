# Generated by Django 5.2.1 on 2025-05-23 09:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DichVu',
            fields=[
                ('ma_dv', models.AutoField(primary_key=True, serialize=False)),
                ('ten_dv', models.CharField(max_length=50)),
                ('mo_ta', models.TextField()),
                ('phi_dv', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('anh_dai_dien', models.ImageField(upload_to='dich_vu/')),
                ('hoat_dong', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DonDatPhong',
            fields=[
                ('ma_ddp', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_dat', models.DateTimeField(auto_now_add=True)),
                ('ngay_nhan', models.DateField()),
                ('ngay_tra', models.DateField()),
                ('so_luong_nguoi', models.PositiveIntegerField(default=1)),
                ('gia_ddp', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('trang_thai', models.CharField(choices=[('cho_xac_nhan', 'Chờ xác nhận'), ('da_xac_nhan', 'Đã xác nhận'), ('da_checkin', 'Đã check-in'), ('da_checkout', 'Đã check-out'), ('da_huy', 'Đã hủy')], default='cho_xac_nhan', max_length=20)),
                ('ghi_chu', models.TextField(blank=True)),
                ('da_thanh_toan', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Phong',
            fields=[
                ('ma_p', models.AutoField(primary_key=True, serialize=False)),
                ('ten_p', models.CharField(max_length=50, unique=True)),
                ('gia', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('loai_p', models.CharField(choices=[('standard', 'Phòng Standard'), ('deluxe', 'Phòng Deluxe'), ('suite', 'Phòng Suite'), ('family', 'Phòng Gia đình')], max_length=25)),
                ('chinh_sach_huy_p', models.TextField()),
                ('mo_ta', models.TextField()),
                ('anh_dai_dien', models.ImageField(upload_to='phong/')),
                ('trang_thai', models.CharField(choices=[('trong', 'Trống'), ('da_dat', 'Đã đặt'), ('dang_su_dung', 'Đang sử dụng'), ('bao_tri', 'Bảo trì')], default='trong', max_length=20)),
                ('suc_chua', models.PositiveIntegerField(default=2)),
                ('tien_ich', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DonDatDichVu',
            fields=[
                ('ma_ddv', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_su_dung', models.DateField()),
                ('gio_su_dung', models.TimeField()),
                ('so_luong', models.PositiveIntegerField(default=1)),
                ('thanh_tien', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('ghi_chu', models.TextField(blank=True)),
                ('dich_vu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.dichvu')),
                ('don_dat_phong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.dondatphong')),
            ],
        ),
        migrations.CreateModel(
            name='HoaDon',
            fields=[
                ('ma_hd', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('tong_tien', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('da_thanh_toan', models.BooleanField(default=False)),
                ('phuong_thuc_tt', models.CharField(blank=True, max_length=50)),
                ('ghi_chu', models.TextField(blank=True)),
                ('don_dat_phong', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.dondatphong')),
            ],
        ),
        migrations.CreateModel(
            name='KhachHang',
            fields=[
                ('ma_kh', models.AutoField(primary_key=True, serialize=False)),
                ('ten_kh', models.CharField(max_length=50)),
                ('sdt', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('dia_chi', models.TextField()),
                ('anh_dai_dien', models.ImageField(blank=True, null=True, upload_to='khach_hang/')),
                ('ghi_chu', models.TextField(blank=True)),
                ('tai_khoan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dondatphong',
            name='khach_hang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.khachhang'),
        ),
        migrations.CreateModel(
            name='NhanVien',
            fields=[
                ('ma_nv', models.AutoField(primary_key=True, serialize=False)),
                ('ten_nv', models.CharField(max_length=50)),
                ('gioi_tinh', models.CharField(choices=[('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], max_length=10)),
                ('sdt', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('dia_chi', models.TextField()),
                ('vi_tri', models.CharField(choices=[('le_tan', 'Lễ tân'), ('buong_phong', 'Buồng phòng'), ('phuc_vu', 'Phục vụ'), ('quan_ly', 'Quản lý'), ('ky_thuat', 'Kỹ thuật')], max_length=30)),
                ('trang_thai', models.CharField(choices=[('dang_lam', 'Đang làm'), ('nghi_viec', 'Nghỉ việc'), ('nghi_phep', 'Nghỉ phép')], default='dang_lam', max_length=20)),
                ('ngay_vao_lam', models.DateField()),
                ('anh_dai_dien', models.ImageField(blank=True, null=True, upload_to='nhan_vien/')),
                ('tai_khoan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dondatphong',
            name='phong',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.phong'),
        ),
        migrations.CreateModel(
            name='AnhPhong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anh', models.ImageField(upload_to='phong_phu/')),
                ('mo_ta_anh', models.CharField(blank=True, max_length=200, null=True, verbose_name='Mô tả ảnh')),
                ('phong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anh_phu', to='core.phong')),
            ],
        ),
        migrations.CreateModel(
            name='YeuCau',
            fields=[
                ('ma_yc', models.AutoField(primary_key=True, serialize=False)),
                ('loai_yc', models.CharField(choices=[('buong_phong', 'Buồng phòng'), ('ky_thuat', 'Kỹ thuật'), ('phuc_vu', 'Phục vụ'), ('le_tan', 'Lễ tân'), ('khac', 'Khác')], max_length=20)),
                ('noi_dung_yc', models.TextField()),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('ngay_cap_nhat', models.DateTimeField(auto_now=True)),
                ('tinh_trang', models.CharField(choices=[('cho_phan_cong', 'Chưa phân công'), ('da_phan_cong', 'Đã phân công'), ('dang_xu_ly', 'Đang xử lý'), ('da_xu_ly', 'Đã xử lý'), ('da_huy', 'Đã hủy')], default='cho_phan_cong', max_length=30)),
                ('thoi_gian_hoan_thanh', models.DateTimeField(blank=True, null=True)),
                ('ghi_chu', models.TextField(blank=True)),
                ('khach_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.khachhang')),
                ('nhan_vien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.nhanvien')),
                ('phong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.phong')),
            ],
        ),
        migrations.CreateModel(
            name='LichLamViec',
            fields=[
                ('ma_lich', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_lam', models.DateField()),
                ('ca_lam', models.CharField(choices=[('sang', 'Ca sáng (6h30-11h)'), ('chieu', 'Ca chiều (11h-17h)'), ('toi', 'Ca tối (17h-22h)'), ('khuya', 'Ca khuya (22h-7h)')], max_length=20)),
                ('ghi_chu', models.TextField(blank=True)),
                ('nhan_vien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.nhanvien')),
            ],
            options={
                'unique_together': {('nhan_vien', 'ngay_lam', 'ca_lam')},
            },
        ),
    ]
