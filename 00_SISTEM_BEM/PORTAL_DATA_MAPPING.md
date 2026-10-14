# 📊 PORTAL LK-FEB — Master Data Mapping
**Pemetaan Data dari `bem_feb_data_master.xlsx` ke Supabase Schema**

---

## 📋 Overview

Dokumen ini mendeskripsikan transformasi data dari format spreadsheet Excel (`bem_feb_data_master.xlsx`) ke struktur relational database Supabase (PostgreSQL). Setiap sheet Excel dipetakan ke satu atau lebih tabel di database.

---

## 🗺️ Sheet-to-Table Mapping

### Sheet 1: "Timeline BEM FEB UKRIDA 26"
**📥 Sumber**: Kolom: Task Title, Task Owner, Start Date, Due Date, Duration, Status, Jobs Component, File, Keterangan  
**📤 Tabel Target**: `timeline_tasks`, `task_assignments`

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| No | id (auto) | UUID | PK | Auto-generate |
| TASK TITLE | task_title | TEXT | NOT NULL | Judul task/proker |
| TASK OWNER | task_owner | TEXT[] | - | Array: [nama1, nama2, ...] |
| START DATE | start_date | DATE | - | Tgl mulai |
| DUE DATE | due_date | DATE | - | Tgl target selesai |
| DURATION | duration | INTEGER | - | Hari (auto-calc: due_date - start_date) |
| STATUS | status | TEXT | CHECK(...) | 'Not Started' / 'On progress' / 'Completed' / 'OFF TRACK' |
| JOBS COMPONENT | jobs_component | TEXT | - | Kategori: "Project Management", "Administration", "Logistic", etc |
| FILE | file_reference | TEXT | - | Link ke dokumen/spreadsheet |
| KETERANGAN | keterangan | TEXT | - | Catatan tambahan |

**Proses Migrasi**:
1. Extract 11 task utama (Proker Umum, PPK ORMAWA, Oprec, Goes To School, LKMM, PKKMB, HSGT, Economic Day, Podcast, Optik Melawai, Anggaran Proker)
2. Parse task_owner menjadi array NIM yang akan di-lookup dari tabel `members`
3. Calculate duration otomatis jika kosong
4. Insert ke `timeline_tasks` dengan status enum validation

---

### Sheet 2: "Jadwal Kelas"
**📥 Sumber**: Kolom: Hari, Jam, dan grid jam kelas per hari (Senin-Sabtu)  
**📤 Tabel Target**: `class_schedule` (Optional - untuk tracking ketersediaan anggota)

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| Hari | day_of_week | TEXT | CHECK | 'Senin', 'Selasa', ... |
| Jam | time_slot | TEXT | - | Format: "08:00-10:30" |
| Status (yang tidak bisa) | availability | BOOLEAN | - | FALSE jika tidak tersedia |

**Proses Migrasi**:
- Data ini optional untuk Phase 1; dapat dilewat untuk Phase 0
- Berguna untuk koordinasi rapat & event scheduling phase-to-come

---

### Sheet 3: "KEUANGAN BEM FEB"
**📥 Sumber**: Kolom: Nama Lengkap, Bulan (Mei-Februari), nilai TRUE/FALSE  
**📤 Tabel Target**: `finance`

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| Nama Lengkap | member_id | UUID FK | NOT NULL | Reference ke `members.id` via lookup NIM |
| Mei 26 - Februari | bulan | TEXT | NOT NULL | Format: "Mei", "Juni", ... atau "05", "06", ... |
| [TRUE/FALSE] | status_bayar | BOOLEAN | - | TRUE = sudah bayar kas, FALSE = belum |
| Tahun | tahun | INTEGER | - | 2026 (implicit) |

**Proses Migrasi**:
1. Normalisasi: Ubah dari wide format (bulan per kolom) menjadi long format (satu baris per bulan per member)
2. Lookup member_id dari `members.nim` melalui tabel `members`
3. Parse TRUE/FALSE menjadi BOOLEAN
4. Insert ke `finance` dengan (member_id, bulan, tahun, status_bayar)

**Contoh Transformasi**:
```
BEFORE (Wide):
| Nama | Mei 26 | Juni 26 | Juli 26 |
| Arthur | TRUE | TRUE | FALSE |

AFTER (Long - 3 baris):
| member_id | bulan | tahun | status_bayar |
| uuid-1 | 05 | 2026 | true |
| uuid-1 | 06 | 2026 | true |
| uuid-1 | 07 | 2026 | false |
```

---

### Sheet 4: "BAGAN STRUKTUR KEPENGURUSAN BEM"
**📥 Sumber**: Hirarki Ketua → Wakil Ketua → Divisi → Koordinator → Anggota  
**📤 Tabel Target**: `organizational_structure` atau relasi dalam `members.jabatan`

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| Jabatan | jabatan | TEXT | NOT NULL | 'Ketua', 'Wakil Ketua', 'Sekretaris', 'Bendahara', 'Koor [Divisi]', 'Anggota [Divisi]' |
| Nama | member_id | UUID FK | - | Reference ke `members.id` |
| Divisi | divisi | TEXT | - | 'HUMAS', 'BD', 'Event', 'Pubdoc', 'HR', 'LO', etc |

**Proses Migrasi**:
- Sudah ter-capture di tabel `members` via kolom `jabatan` dan `divisi`
- Jika diperlukan struktur hierarki eksplisit, bisa buat tabel `organizational_structure` dengan (parent_member_id, child_member_id, relation_type)

---

### Sheet 5: "ANGGOTA PENGURUS BEM FEB"
**📥 Sumber**: Detail lengkap 20 pengurus BEM FEB 2026/27  
**📤 Tabel Target**: `members`

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| No | id (auto) | UUID | PK | Auto-generate |
| Nama | nama_lengkap | TEXT | NOT NULL, UNIQUE | Nama lengkap resmi |
| NIM | nim | TEXT | UNIQUE NOT NULL | Format: 3XXYZZABC (e.g., 312023002) |
| Gmail Utama | email | TEXT | UNIQUE NOT NULL | Email civitas/personal |
| Ulang Tahun | tanggal_lahir | DATE | - | Format: YYYY-MM-DD |
| Alamat | alamat | TEXT | - | Alamat tempat tinggal |
| No Rek | no_rekening | TEXT | - | Nomor rekening (BCA/Mandiri/etc), masked atau encrypted |
| Foto Formal | foto_formal_url | TEXT | - | URL ke Google Drive / Supabase Storage |
| Foto Warna Bebas | foto_divisi_url | TEXT | - | URL ke Google Drive / Supabase Storage |
| Jurusan (Tahun) | jurusan | TEXT | - | Format: "Manajemen (23)" → Parse ke `jurusan` & `tahun_masuk` |
| Jabatan | jabatan | TEXT | NOT NULL | 'Ketua BEM', 'Wakil Ketua', 'Sekretaris', 'Bendahara', 'Koor [Divisi]', 'Anggota [Divisi]' |

**Proses Migrasi**:
1. Extractdata dari kolom No 1-20 (Arthur Reezan s/d Jessy)
2. Parse kolom "Jurusan (Tahun)" menjadi separate fields: `jurusan`, `tahun_masuk`
3. Generate `status` default: "active" (jika masih pengurus saat ini)
4. Download foto dari Google Drive link & upload ke Supabase Storage, simpan URL baru
5. Insert ke `members` dengan all fields populated

**Contoh Parsed Data (Arthur Reezan)**:
```json
{
  "id": "uuid-1",
  "nama_lengkap": "Arthur Reezan",
  "nim": "312023002",
  "email": "ziarssssavantris@gmail.com",
  "tanggal_lahir": "1970-01-20",  // Derived from Ulang Tahun = 38584
  "alamat": "Duta Bandara Permai Gs 1 no 16",
  "no_rekening": "7580869925",
  "jurusan": "Manajemen",
  "tahun_masuk": 2023,
  "jabatan": "Ketua BEM",
  "divisi": null,
  "foto_formal_url": "https://supabase.../photos/arthur_formal.jpg",
  "foto_divisi_url": null,
  "status": "active",
  "created_at": "2026-10-14T04:48:24.552Z"
}
```

---

### Sheet 6: "Target Media Partner"
**📥 Sumber**: 18 media partner yang ditargetkan  
**📤 Tabel Target**: `sponsors` (dengan kategori = 'media_partner')

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| No | id (auto) | UUID | PK | Auto-generate |
| Nama | nama | TEXT | NOT NULL, UNIQUE | Nama organisasi media |
| Telp | telepon | TEXT | - | Nomor telepon hubungi |
| Email | email | TEXT | - | Email resmi |
| Tanggal | tanggal_pendekatan | DATE | - | Tgl first contact |
| Respon | status_respon | TEXT | - | 'Sudah ada respon' / 'Belum ada respon' / 'Memerlukan KTP' / etc |
| Tanggal Follow Up | tanggal_followup | DATE | - | Tgl follow-up terakhir |
| Keterangan | keterangan | TEXT | - | Catatan kerja sama (terms & conditions) |
| Kategori (implicit) | kategori | TEXT | - | 'media_partner' (hard-coded) |

**Proses Migrasi**:
1. Extract 18 media partner (Indoesports, Revival TV, Suara.com, ... , Tokopedia, Dana, etc)
2. Parse Tanggal dari format Excel serial (46129.0 → 2026-05-11)
3. Insert ke `sponsors` dengan kategori='media_partner'

---

### Sheet 7: "Target Sponsor"
**📥 Sumber**: 72 sponsor perusahaan/institusi yang ditargetkan  
**📤 Tabel Target**: `sponsors` (dengan kategori = 'sponsor')

| Excel Column | DB Column | Type | Validasi | Catatan |
|---|---|---|---|---|
| No | id (auto) | UUID | PK | Auto-generate |
| Nama | nama | TEXT | NOT NULL | Nama sponsor (perusahaan/bank/brand) |
| Telp | telepon | TEXT | - | Nomor telepon |
| Email | email | TEXT | - | Email kontak |
| Tanggal | tanggal_pendekatan | DATE | - | Tgl approach pertama |
| Respon | status_respon | TEXT | - | 'Belum ada respon' / 'Sudah ada respon' / 'Menunggu ...' / 'Gagal' / etc |
| Tanggal Follow Up | tanggal_followup | DATE | - | Tgl follow-up terbaru |
| Keterangan | keterangan | TEXT | - | Catatan (respon detail, alasan gagal, terms) |
| Kategori (implicit) | kategori | TEXT | - | 'sponsor' (hard-coded) |

**Proses Migrasi**:
1. Extract 72 sponsor (PS Enterprise, Booyah Indonesia, Axis/XL, Bank Mandiri, ... , Tiktok, Samsung, etc)
2. Normalize date fields
3. Insert ke `sponsors` dengan kategori='sponsor'

---

## 🔄 Data Transformation Pipeline

### Tahap 1: Extract
```python
import pandas as pd

# Baca Excel master file
xls = pd.ExcelFile('bem_feb_data_master.xlsx')
print(xls.sheet_names)

# Extract individual sheets
timeline_df = pd.read_excel(xls, sheet_name='Timeline BEM FEB UKRIDA 26')
members_df = pd.read_excel(xls, sheet_name='ANGGOTA PENGURUS BEM FEB')
finance_df = pd.read_excel(xls, sheet_name='KEUANGAN BEM FEB')
sponsors_df = pd.read_excel(xls, sheet_name=['Target Media Partner', 'Target Sponsor'])
```

### Tahap 2: Transform
```python
# Contoh transformasi finance (wide → long)
finance_long = finance_df.melt(
    id_vars=['Nama Lengkap'],
    value_vars=['Mei 26', 'Juni 26', 'Juli 26', ...],
    var_name='bulan',
    value_name='status_bayar'
)

# Lookup member_id dari members_df
finance_long = finance_long.merge(
    members_df[['Nama', 'NIM', 'id']],
    left_on='Nama Lengkap',
    right_on='Nama',
    how='left'
)
```

### Tahap 3: Load
```python
from supabase import create_client
import os

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

# Insert ke Supabase
for index, row in finance_long.iterrows():
    supabase.table('finance').insert({
        'member_id': row['id'],
        'bulan': row['bulan'],
        'tahun': 2026,
        'status_bayar': bool(row['status_bayar'])
    }).execute()
```

---

## ⚠️ Data Quality & Validation

### Checks Pre-Migration
- [ ] No NULL values in PK fields (id, nim, email, etc)
- [ ] NIM format valid & unique (3XXYZZABC pattern)
- [ ] Email format valid & unique
- [ ] Date fields parseable (no invalid dates)
- [ ] Foreign key references resolvable (member_id lookup, divisi valid, etc)
- [ ] Numeric fields sanitized (no symbols, valid ranges)

### Checks Post-Migration
- [ ] Row count matches pre-migration (no data loss)
- [ ] PK uniqueness verified
- [ ] FK relationships valid (no orphaned records)
- [ ] RLS policies working correctly

---

## 📅 Migration Schedule (Phase 2)

| Week | Task | Owner | Status |
|---|---|---|---|
| W1 (Mar 2027) | Finalize Supabase schema & DDL | @lk-formatter | ⏳ Pending |
| W2 (Mar 2027) | Extract & validate data dari Excel | @lk-formatter | ⏳ Pending |
| W3 (Mar 2027) | Build ETL scripts & test transforms | @lk-formatter | ⏳ Pending |
| W4 (Mar 2027) | Load ke Supabase staging & verify | @lk-formatter | ⏳ Pending |
| W1 (Apr 2027) | UAT & business validation | @lk-auditor, @lk-orchestrator | ⏳ Pending |
| W2 (Apr 2027) | Migrate to production & sanity check | @lk-formatter | ⏳ Pending |

---

**Dokumen ini dirawat oleh @lk-arsiparis sebagai bagian dari Technical Documentation Portal LK-FEB.**  
**Last Updated**: 14 Oktober 2026  
**Status**: 🟡 Draft (Menunggu input @lk-formatter untuk schema finalization)
