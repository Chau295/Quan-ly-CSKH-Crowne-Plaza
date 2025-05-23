from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import *
from accounts.models import TaiKhoan
from django.utils import timezone
from datetime import timedelta, date


class PhongForm(forms.ModelForm):
    class Meta:
        model = Phong
        fields = '__all__'
        widgets = {
            'mo_ta': forms.Textarea(attrs={'rows': 3}),
            'chinh_sach_huy_p': forms.Textarea(attrs={'rows': 3}),
            'tien_ich': forms.Textarea(attrs={'rows': 3}),
        }
# Sử dụng inlineformset_factory sẽ tiện hơn khi làm việc với model cha (Phong)
AnhPhongFormSet = inlineformset_factory(
    Phong,  # Model cha
    AnhPhong,  # Model con
    fields=('anh', 'mo_ta_anh'), # Các trường từ AnhPhong muốn hiển thị trong form
    extra=3,  # Số lượng form trống để thêm ảnh mới (có thể điều chỉnh)
    can_delete=True, # Cho phép xóa các ảnh hiện có
    # widgets={'mo_ta_anh': forms.TextInput(attrs={'class': 'form-control form-control-sm'})} # Tùy chỉnh widget nếu cần
)

class AnhPhongForm(forms.ModelForm): # Một form riêng cho AnhPhong nếu cần xử lý AJAX hoặc custom
    class Meta:
        model = AnhPhong
        fields = ('anh', 'mo_ta_anh')
        widgets = {
            'mo_ta_anh': forms.TextInput(attrs={'placeholder': 'Mô tả ngắn cho ảnh (tùy chọn)'}),
        }

class DichVuForm(forms.ModelForm):
    class Meta:
        model = DichVu
        fields = '__all__'
        widgets = {
            'mo_ta': forms.Textarea(attrs={'rows': 3}),
        }


class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = '__all__'
        exclude = ['tai_khoan']


class NhanVienForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = '__all__'
        exclude = ['tai_khoan']
        widgets = {
            'ngay_vao_lam': forms.DateInput(attrs={'type': 'date'}),
            'dia_chi': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password'] = forms.CharField(
            widget=forms.PasswordInput(),
            required=False,
            label="Đổi mật khẩu",
            help_text="Để trống nếu không muốn thay đổi"
        )

    def clean_sdt(self):
        sdt = self.cleaned_data.get('sdt')
        if len(sdt) != 10 or not sdt.isdigit():
            raise forms.ValidationError("Số điện thoại phải có 10 chữ số")
        return sdt

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not "@" in email:
            raise forms.ValidationError("Email không hợp lệ")
        return email


class AddNhanVienForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Tên đăng nhập")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Mật khẩu")

    class Meta:
        model = NhanVien
        exclude = ['tai_khoan']
        widgets = {
            'ngay_vao_lam': forms.DateInput(attrs={'type': 'date'}),
            'dia_chi': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_sdt(self):
        sdt = self.cleaned_data.get('sdt')
        if len(sdt) != 10 or not sdt.isdigit():
            raise forms.ValidationError("Số điện thoại phải có 10 chữ số")
        return sdt

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if TaiKhoan.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại")
        return username


class EditNhanVienForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Đổi mật khẩu",
        help_text="Để trống nếu không muốn thay đổi"
    )

    class Meta:
        model = NhanVien
        exclude = ['tai_khoan']
        widgets = {
            'ngay_vao_lam': forms.DateInput(attrs={'type': 'date'}),
            'dia_chi': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_sdt(self):
        sdt = self.cleaned_data.get('sdt')
        if len(sdt) != 10 or not sdt.isdigit():
            raise forms.ValidationError("Số điện thoại phải có 10 chữ số")
        return sdt


class LichLamViecForm(forms.ModelForm):
    class Meta:
        model = LichLamViec
        fields = '__all__'
        widgets = {
            'ngay_lam': forms.DateInput(attrs={'type': 'date'}),
            'ghi_chu': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nhan_vien = cleaned_data.get('nhan_vien')
        ngay_lam = cleaned_data.get('ngay_lam')
        ca_lam = cleaned_data.get('ca_lam')

        if ngay_lam is None:
            raise forms.ValidationError("Vui lòng chọn ngày làm việc")

        if ngay_lam < date.today():
            raise forms.ValidationError("Không thể tạo lịch làm việc trong quá khứ")

        if LichLamViec.objects.filter(nhan_vien=nhan_vien, ngay_lam=ngay_lam, ca_lam=ca_lam).exists():
            raise ValidationError("Nhân viên đã có lịch làm việc trong ca này")

        return cleaned_data


class DonDatPhongForm(forms.ModelForm):
    class Meta:
        model = DonDatPhong
        fields = ['phong', 'ngay_nhan', 'ngay_tra', 'so_luong_nguoi', 'ghi_chu', 'khach_hang']
        widgets = {
            'ngay_nhan': forms.DateInput(attrs={'type': 'date'}),
            'ngay_tra': forms.DateInput(attrs={'type': 'date'}),
            'ghi_chu': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['khach_hang'].required = False

    def clean(self):
        cleaned_data = super().clean()
        phong = cleaned_data.get('phong')
        ngay_nhan = cleaned_data.get('ngay_nhan')
        ngay_tra = cleaned_data.get('ngay_tra')
        so_luong_nguoi = cleaned_data.get('so_luong_nguoi')

        if ngay_nhan and ngay_tra:
            if ngay_nhan >= ngay_tra:
                raise ValidationError("Ngày trả phòng phải sau ngày nhận phòng")

            if (ngay_tra - ngay_nhan).days > 30:
                raise ValidationError("Không thể đặt phòng quá 30 ngày")

            conflicting_bookings = DonDatPhong.objects.filter(
                phong=phong,
                ngay_nhan__lt=ngay_tra,
                ngay_tra__gt=ngay_nhan,
                trang_thai__in=['da_xac_nhan', 'da_checkin']
            )
            if conflicting_bookings.exists():
                raise ValidationError("Phòng đã được đặt trong khoảng thời gian này")

        if so_luong_nguoi and phong:
            if so_luong_nguoi > phong.suc_chua:
                raise ValidationError(f"Phòng này chỉ chứa tối đa {phong.suc_chua} người")

        return cleaned_data


class DonDatDichVuForm(forms.ModelForm):
    class Meta:
        model = DonDatDichVu
        fields = ['dich_vu', 'ngay_su_dung', 'gio_su_dung', 'so_luong', 'ghi_chu']
        widgets = {
            'ngay_su_dung': forms.DateInput(attrs={'type': 'date'}),
            'gio_su_dung': forms.TimeInput(attrs={'type': 'time'}),
            'ghi_chu': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        don_dat_phong = self.instance.don_dat_phong if self.instance else None
        ngay_su_dung = cleaned_data.get('ngay_su_dung')
        so_luong = cleaned_data.get('so_luong')

        if don_dat_phong and ngay_su_dung:
            if ngay_su_dung < don_dat_phong.ngay_nhan or ngay_su_dung > don_dat_phong.ngay_tra:
                raise ValidationError("Ngày sử dụng dịch vụ phải nằm trong khoảng thời gian thuê phòng")

        if so_luong and so_luong <= 0:
            raise ValidationError("Số lượng phải lớn hơn 0")

        return cleaned_data


class YeuCauForm(forms.ModelForm):
    class Meta:
        model = YeuCau
        fields = ['loai_yc', 'noi_dung_yc', 'ghi_chu']
        widgets = {
            'noi_dung_yc': forms.Textarea(attrs={'rows': 3}),
            'ghi_chu': forms.Textarea(attrs={'rows': 3}),
        }


class KhachHangProfileForm(forms.ModelForm):
    """
    Form chỉ xử lý upload ảnh đại diện cho Khách hàng.
    """
    class Meta:
        model = KhachHang
        fields = ['anh_dai_dien']
        widgets = {
            'anh_dai_dien': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class NhanVienProfileForm(forms.ModelForm):
    """
    Form chỉ xử lý upload ảnh đại diện cho Nhân viên.
    """
    class Meta:
        model = NhanVien
        fields = ['anh_dai_dien']
        widgets = {
            'anh_dai_dien': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


def ProfileEditForm(*args, **kwargs):
    """
    Factory trả về form phù hợp dựa vào instance:
      - Nếu instance là KhachHang, trả về KhachHangProfileForm
      - Nếu instance là NhanVien, trả về NhanVienProfileForm
    Sử dụng:
      form = ProfileEditForm(request.POST, request.FILES, instance=instance)
    """
    instance = kwargs.get('instance', None)
    if isinstance(instance, KhachHang):
        return KhachHangProfileForm(*args, **kwargs)
    elif isinstance(instance, NhanVien):
        return NhanVienProfileForm(*args, **kwargs)
    raise ValueError('ProfileEditForm requires instance of KhachHang or NhanVien')
