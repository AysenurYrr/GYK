---------------------------------------------------------------LEVEL 1-----------------------------------------------------------------------
-- 1) En Çok Satış Yapan Çalışanı Bulun Her çalışanın (Employees) sattığı toplam ürün adedini hesaplayarak, en çok satış yapan ilk 3 çalışanı listeleyen bir sorgu yazınız. 
   select * from employees
   select * from orders -- employee_id

   select e.first_name, e.last_name,count(o.order_id) 
   from employees e inner join orders o on e.employee_id= o.employee_id 
   group by e.first_name, e.last_name order by count(o.order_id) desc limit 3
     
-- 2) Aylık Satış Trendlerini Bulun Siparişlerin (Orders) hangi yıl ve ayda ne kadar toplam satış geliri oluşturduğunu hesaplayan ve yıllara göre sıralayan bir sorgu yazınız.
-- extract(year from o.order_date) --> Tarih kısmında yazılı olan yıl bilgisini almaya yarar. Sadece yılı alır bu sayede   
   
   select * from orders
   select * from order_details -- order_id

   select sum(od.unit_price*od.quantity) as total_price,
   extract(year from o.order_date) as order_year, 
   extract(month from o.order_date) as order_month
   from orders o inner join order_details od on o.order_id=od.order_id
   group by
   extract(year from o.order_date), 
   extract(month from o.order_date)
   order by order_year desc, order_month desc
   
-- 3) En Karlı Ürün Kategorisini Bulun Her ürün kategorisinin (Categories), o kategoriye ait ürünlerden (Products) yapılan satışlar sonucunda elde ettiği toplam geliri hesaplayan bir sorgu yazınız.
   select * from order_details --product_id
   select * from categories
   select * from products -- category_id


   select sum(od.unit_price*od.quantity) as total_price,c.category_name
   from categories c 
   inner join products p on c.category_id=p.category_id
   inner join order_details od on p.product_id = od.product_id
   group by c.category_name
   order by total_price desc limit 1

-- 4) Belli Bir Tarih Aralığında En Çok Sipariş Veren Müşterileri Bulun 1997 yılında en fazla sipariş veren ilk 5 müşteriyi listeleyen bir sorgu yazınız.
    select * from customers
	select * from orders --customer_id

	select c.customer_id,c.company_name,count(o.order_id) as total ,extract(year from o.order_date) as order_year 
	from customers c inner join orders o on c.customer_id=o.customer_id
	group by 
	extract(year from o.order_date),c.customer_id,c.company_name 
	having extract(year from o.order_date)=1997
	order by total desc limit 5

-- 5) Ülkelere Göre Toplam Sipariş ve Ortalama Sipariş Tutarını Bulun Müşterilerin bulunduğu ülkeye göre toplam sipariş sayısını ve ortalama sipariş tutarını hesaplayan bir sorgu yazınız. Sonucu toplam sipariş sayısına göre büyükten küçüğe sıralayın.

   select * from customers
   select * from order_details --order_id
   select * from orders --customer_id

   select c.country, count(o.order_id) as total_orders, avg(od.unit_price*od.quantity) as avg_price
   from customers c inner join orders o on c.customer_id=o.customer_id
   inner join order_details od on o.order_id= od.order_id
   group by c.country
   order by total_orders desc

---------------------------------------------------------------LEVEL 2-----------------------------------------------------------------------

-- 1) Her Çalışanın En Çok Satış Yaptığı Ürünü Bulun 
--    Her çalışanın (Employees) sattığı ürünler içinde en çok sattığı (toplam adet olarak) ürünü bulun ve sonucu çalışana göre sıralayın.

-- DISTINCT ON (column1, column2): Belirtilen sütunlar için sadece bir benzersiz satır döndürecektir. 
-- Aynı column1 ve column2 değerlerine sahip tüm satırlardan yalnızca ilk satır seçilecektir.
-- Burada bir adet sanal tablo kullanılmıştır.
-- ilk tabloda gerekli olanlar groub by göre tekrarı onlenerek getirilmiştir.
-- Sonrasında oluşturulan bu tablo distinct on yardımıyla (first name ve last name) satırı birlikte düşünülerek farklı olduğu ilk satıtlar getirilmiştir.
-- sum(od.quantity) kullanabilmek adına  group by kullanılmıştır.

select * from employees
select * from orders -- employee_id
select * from order_details -- order_id, product_id
select * from products

with employee_product_quantity as ( -- Her çalışanın, sattığı ürünlerin toplam kaç adet olduğunu gösteren sanal tablo
  select 
     e.first_name, 
	 e.last_name, 
	 p.product_name, 
	 sum(od.quantity) as total_sales
from employees e
inner join orders o on e.employee_id = o.employee_id
inner join order_details od on o.order_id = od.order_id
inner join products p on p.product_id = od.product_id 
group by e.first_name, e.last_name, p.product_name 
)

select distinct on (first_name, last_name) -- Burada satılan adete göre sıralama yapılarak en üsteki ilk satır gösterilmiştir.
    first_name, 
	last_name, 
	product_name, 
	total_sales
from employee_product_quantity
order by first_name, last_name, total_sales desc
   
-- 2️) Bir Ülkenin Müşterilerinin Satın Aldığı En Pahalı Ürünü Bulun 
--    Belli bir ülkenin (örneğin "Germany") müşterilerinin verdiği siparişlerde satın aldığı en pahalı ürünü (UnitPrice olarak) bulun ve hangi müşterinin aldığını listeleyin.

-- DISTINCT ON (column1, column2) kullanamayız çünkü aynı ülkede en pahalı ürünü almış iki firma olabilir.
-- Burda iki sanal tablo kullanılmıştır.
-- Birinci sanal tablo bize gerekli olan tüm tabloların gerekli kısımlarını getirmek içindir.
-- İkinci sanal tablo ilk tablodan ülke tekrarı olmaksızın sadece en yüksek fiyatların olduğu bir tablodur.
-- Sonuç olarak bu iki tablo inner join ile birleştirilmiştir.
-- co.country = mp.country and co.unit_price = mp.max_unit_price birleştirme işlemi bu kurala göre yapılmıştır. 
-- Busayede ülkeye göre unit_price'ı max olana eşit olan firmaları getirerek veri kay bını önlemiş olduk.

select * from customers
select * from orders -- customer_id
select * from order_details -- order_id, product_id
select * from products

with country_orders as ( -- esas sanal tablo burada customers,orders,order_details ve products tabloları birleştirildi
    select 
        c.customer_id,
        c.company_name,
        p.product_name,
        od.unit_price,
        c.country
    from customers c
    inner join orders o on c.customer_id = o.customer_id
    inner join order_details od on o.order_id = od.order_id
    inner join products p on od.product_id = p.product_id
),
max_price as ( -- En pahalı ürün fiyatı,ile ülke sanal tablosu ama sıralaması ülkeye göre
    select 
	  country, 
	  max(unit_price) as max_unit_price
    from country_orders
    group by country
)
select 
  co.customer_id, 
  co.company_name, 
  co.product_name, 
  co.unit_price, 
  co.country
from country_orders co
inner join max_price mp on co.country = mp.country and co.unit_price = mp.max_unit_price
group by co.customer_id, co.company_name, co.product_name, co.unit_price, co.country -- bunu yaptık çünkü tekrarlılarıda gösteriyordu bi firma aynı ürünü iki defa almış.
order by co.country, co.company_name

-- 3️) Her Kategoride (Categories) En Çok Satış Geliri Elde Eden Ürünü Bulun 
--    Her kategori için toplam satış geliri en yüksek olan ürünü bulun ve listeleyin.

select * from categories
select * from products -- category_id

with sales_by_category as ( -- Categories ile Products tabloları birleştirilmiştir ve her ürünün toplam satış geliti hesaplanmıştır.
    select 
        p.category_id,
        p.product_name,
        (od.unit_price * od.quantity) as total_sales
    from products p
    inner join order_details od on p.product_id = od.product_id
), 
max_sales as ( -- Üsteki sanal tablo category_id göre grouplanalarak, ürününlerin maximum satış gelirleri satır olarak eklenmiştir. Busayede her kategorinin max satış geliri getiren ürününün geliri yazdırılmıştır.
    select
        category_id,
        max(total_sales) as max_sales
    from sales_by_category
    group by category_id
)
select -- Burada üste oluşturulan iki sanal taplo categoriy_id ile birleştirilmiştir.
    s.category_id,
    s.product_name,
    s.total_sales
from sales_by_category s
inner join max_sales m on s.category_id = m.category_id
where s.total_sales = m.max_sales -- Where koşuluna ise max satış geri ile satış geliri aynı olanları getirmesi istenmiştir. Böylece sadece max olanlar gelicektir.
group by s.category_id,s.product_name,s.total_sales -- Tekrarı önlemek adına yapılmıştır.
order by s.category_id  -- category_id küçükten büyüğe sıralayarak gösterilmiştir.

-- 4️) Arka Arkaya En Fazla Sipariş Veren Müşteriyi Bulun 
--    Sipariş tarihleri (OrderDate) baz alınarak arka arkaya en fazla sipariş veren müşteriyi bulun. 
--    (Örneğin, bir müşteri ardışık günlerde kaç sipariş vermiş?)

select * from customers
select * from orders

with order_dates as (
    select 
        customer_id,
        order_date,
        row_number() over (partition by customer_id order by order_date) as row_num
    from orders
),
gaps as (
    select
        customer_id,
        order_date,
        row_num - row_number() over (partition by customer_id order by order_date) as gap_group
    from order_dates
)
select
    customer_id,
    count(*) as consecutive_orders
from gaps
group by customer_id, gap_group
order by consecutive_orders desc

-- 5) Çalışanların Sipariş Sayısına Göre Kendi Departmanındaki Ortalamanın Üzerinde Olup Olmadığını Belirleyin 
--    Her çalışanın aldığı sipariş sayısını hesaplayın ve kendi departmanındaki çalışanların ortalama sipariş sayısıyla karşılaştırın. 
--    Ortalama sipariş sayısının üstünde veya altında olduğunu belirten bir sütun ekleyin.

select * from employees
select * from orders -- employee_id

with employee_orders as (  -- Her çalışanın sipariş sayısını göstermek için bir sanal tablo oluşturduk.
    select 
        e.employee_id,
        e.first_name,
        e.last_name,
        e.title,
        count(o.order_id) as order_count
    from employees e
    inner join orders o on e.employee_id = o.employee_id
    group by e.employee_id, e.first_name, e.last_name, e.title
), 
title_avg as (   -- Title (pozisyona göre) ortalama sipariş sayısını hesaplayıp gösteren  tablo
    select 
        title,
        avg(order_count) as avg_order_count
    from employee_orders
    group by title
)
select  -- Bu sorguda üste oluşturulan iki sanal tablo birleştirilmiştir.
    eo.employee_id,
    eo.first_name,
    eo.last_name,
    eo.title,
    eo.order_count,
    ta.avg_order_count,
    case -- Bir çeşit karşılaştırma komutu
        when eo.order_count > ta.avg_order_count then 'Üstünde' -- ilk sanal tablodaki order_count, ikinci sanal tabloda hesaplanan ortalamadan büyükse üstünde yazar.
        when eo.order_count < ta.avg_order_count then 'Altında'
        else 'Eşit'  -- üsteki hiçbir kurala uymuyorsa eşit yazar.
    end as durum
from employee_orders eo
inner join title_avg ta on eo.title = ta.title -- tablolar title göre birleştirilmiştir
order by eo.title, eo.order_count desc


----------------------------------------------------------------------LEVEL 3

-- LIMIT: Kaç tane satır getirileceğini belirler. (Sadece limit kullanılırsa ilk satırları getirir.) LIMIT 3 dersek ilk 3 satırı getirir.
-- OFFSET: Bir sorgunun döndürdüğü satırların kaçıncı satırdan itibaren getirileceğini belirler.
-- LIMIT 10 OFFSET 0 (İlk 10 kayıt)
-- LIMIT 10 OFFSET 10 (11-20 arasındaki kayıtlar)
-- LIMIT 10 OFFSET 20 (21-30 arasındaki kayıtlar)

-- KULLANIM 1
-- SELECT * FROM tablo_adi
-- ORDER BY sütun_adi
-- LIMIT satır_sayısı OFFSET başlangıç_sayısı;

--------------------------------------------------------------- CTE (Common Table Expressions) ---------------------------------------------------

-- SQL'de WITH ifadesiyle oluşturulan geçici bir sorgu bloğudur. 
-- Bize sanal tablo oluşturmamızı sağlar.
-- Oluşturulan bu tablo sadece o sorgu içinde kullanılabilir.

-- CTE'nin Avantajları
   -- Okunabilirlik: Karmaşık sorguları daha anlaşılır hale getirir.
   -- Kod Tekrarını Azaltma: Aynı alt sorguyu tekrar tekrar yazmaktan kaçınmanızı sağlar.
   -- Recursive (Özyinelemeli) Kullanım: Kendi kendini çağırabilen sorgular oluşturabilirsiniz.
   -- Performans İyileştirme: Büyük ve karmaşık sorgular için optimize edilmiş planlar oluşturulmasına yardımcı olabilir.

-- CTE Kullanılırken dikkat edilmesi gerekenler
   -- CTE İçinde ORDER BY Kullanımı
       -- CTE içinde ORDER BY sadece LIMIT veya OFFSET ile anlamlıdır.
       -- ORDER BY sanal tablonun dış sorgusunda kullanılırsa anlamlaıdır.
   -- CTE İçinde UPDATE, DELETE, INSERT Kullanımı
       -- Yalnızca "Writable CTE" olarak adlandırılan özel bir yapı ile kullanılabilir.
	   -- KULLANIM
	    WITH deneme AS (
		-- Sanal tablo istediğiniz select sorgusunu yazın. order by kullanmayın
	         )
       SELECT * FROM deneme -- sanal tablonun dış sorgusu
   -- CTE İçinde HAVING Tek Başına Kullanılamaz. GROUP BY ile birlikte kullanılmalıdır.
   -- Recursive CTE İçinde DISTINCT Kullanılamaz. Dış sorguda kullanılır.
  
---------------------------------------------------------------------- Windows functions -----------------------------------------------------------------

-- Satır bazlı hesaplamalar yapmamızı sağlayan fonksiyonlardır.
-- Pencere Fonksiyonları:
-- Pencere fonksiyonları, sıralama veya gruplama gerektiren verilerde, belirli hesaplamalar yapmanızı sağlar.
   -- ROW_NUMBER(): Her satıra bir sıralama numarası verir.
   -- LAG(): Bir satırın önceki satırındaki değeri alır.
   -- LEAD(): Bir satırın sonraki satırındaki değeri alır.
   -- RANK(): Satırları sıralayarak, her satır için sıralama numarası verir.
   -- SUM(), AVG(), COUNT(), vb.: Belirli bir pencere için toplam, ortalama, sayma gibi hesaplamalar yapar.
-- Kullanımı:
   window_function() OVER (PARTITION BY column_name ORDER BY column_name)
   -- window_function(): Kullanmak istediğiniz pencere fonksiyonu (örneğin, ROW_NUMBER(), LAG(), SUM(), vb.).
   -- PARTITION BY (isteğe bağlı): Veriyi gruplandırarak, her grup için pencere fonksiyonunun çalışmasını sağlar. 
   -- Eğer PARTITION BY kullanılmazsa, fonksiyon tüm veri kümesi üzerinde çalışır.
   -- ORDER BY: Verilerin sıralanacağı sütun. Fonksiyonun nasıl çalıştığını belirler. Çoğu pencere fonksiyonu, sıralı verilere ihtiyaç duyar.
-- Kullanım Örnekleri:
-- ROW_NUMBER(): Satırlara Sıralama Numarası Verme
select 
    employee_id,
    first_name,
    last_name,
    row_number() over (order by employee_id desc) as row_num
from employees
-- LAG(): Önceki Satırdaki Değeri Almak
select 
    employee_id,
    first_name,
    last_name,
    lag(employee_id) over (order by employee_id) as previous_employee_id
from employees
-- LEAD(): Sonraki Satırdaki Değeri Almak
select 
    employee_id,
    first_name,
    last_name,
    lead(employee_id) over (order by employee_id) as next_employee_id
from employees
-- RANK(): Sıralama Numarası Verme
select 
    employee_id,
    first_name,
    last_name,
    rank() over (order by employee_id) as rank
from employees
-- SUM():Toplam, AVG(): Ortalama
select 
    e.employee_id,
    e.first_name,
    sum(od.unit_price * od.quantity) over (partition by e.employee_id) as total_sales
from employees e
inner join orders o on e.employee_id = o.employee_id
inner join order_details od on o.order_id = od.order_id
-- COUNT(): Sayma
select 
    e.employee_id,
    e.first_name,
    count(o.order_id) over (partition by e.employee_id) as order_count
from employees e
inner join orders o on e.employee_id = o.employee_id

---------------------------------------------------------------------- Recursive queries -----------------------------------------------------------------

-- Recursive Queries (Yinelemeli Sorgular), bir sorgunun kendi kendini tekrar etmesine olanak tanır. 
-- Bu tür sorgular, özellikle hiyerarşik verileri (örneğin ağaç yapıları) sorgularken veya veriyle ilişkili tekrar eden işlemleri çözmek için kullanılır.
-- Özellikle organizasyon şemaları, malzeme listeleri veya dosya sistemleri gibi hiyerarşik veri yapılarıyla uğraşırken kullanışlıdır. 
-- Özyinelemeli sorgular, hiyerarşinin derinliğini veya karmaşıklığını önceden bilmeden bu yapılarda gezinmenize olanak tanır.
-- Özellikleri:
   -- CTE (Common Table Expressions) kullanılır.
   -- İki bölümden oluşur:
       -- Anchor part: Temel başlangıç verisini alır. Yenileme olmayan kısmıdır.
       -- Recursive part: Veriyi sürekli olarak "kendisiyle" birleştirerek işlem yapar, yani aynı CTE’yi tekrar kullanır.

select * from category
select * from products 

with recursive tedarikci_hiyerarsi as (
    -- En üst seviyedeki tedarikçileri seçiyoruz
    select supplier_id, company_name, parent_supplier_id, 0 as seviye
    from suppliers
    where parent_supplier_id is null

    union all

    -- Recursive kısım: Alt tedarikçileri buluyoruz
    select s.supplier_id, s.company_name, s.parent_supplier_id, th.seviye + 1
    from suppliers s
    join tedarikci_hiyerarsi th on s.parent_supplier_id = th.supplier_id
)
select * from tedarikci_hiyerarsi
order by seviye

--------------------------------------------------------------------- Advenced aggregation



------------------------------------------------------------------------- Subqueries



---------------------------------------------------------------------------- Pivot

-- 1) Her Müşteri İçin En Son 3 Siparişi ve Toplam Harcamalarını Listeleyin
--    Her müşterinin en son 3 siparişini (OrderDate’e göre en güncel 3 sipariş) ve bu siparişlerde harcadığı toplam tutarı gösteren bir sorgu yazın.
--    Sonuç müşteri bazında sıralanmalı ve her müşterinin sadece en son 3 siparişi görünmelidir. 

select * from orders
select * from order_details

with customer_order_totals as (
    -- her müşterinin sipariş toplamlarını ve sıralama numarasını hesaplayan CTE
    select 
        o.customer_id, 
        o.order_id, 
        o.order_date, 
        sum(od.unit_price * od.quantity) as order_total,
        -- her müşteri için en son siparişleri sıralamak amacıyla row_number() kullanılıyor
		-- Windows fonksiyonu; partition by o.customer_id yani her customer için bir pencere oluşrurur ve her pencereyi kendi içinde order_date göre sıralayarak gösterir.
        row_number() over (partition by o.customer_id order by o.order_date desc) as rowNumber
    from orders o
    inner join order_details od on o.order_id = od.order_id
    group by o.customer_id, o.order_id, o.order_date
)
-- CTE'den verileri çekiyoruz ve sadece son 3 siparişi listeleyeceğiz
select 
    customer_id, 
    order_id, 
    order_date, 
    order_total
from customer_order_totals
-- sadece rowNumber'ı 3 ve altındaki siparişleri alıyoruz
where rowNumber <= 3
order by customer_id, order_date desc

-- 2️) Aynı Ürünü 3 veya Daha Fazla Kez Satın Alan Müşterileri Bulun.
--    Bir müşteri eğer aynı ürünü (ProductID) 3 veya daha fazla sipariş verdiyse, bu müşteriyi ve ürünleri listeleyen bir sorgu yazın.
--    Aynı ürün bir siparişte değil, farklı siparişlerde tekrar tekrar alınmış olabilir. 

with customer_product_counts as (
    -- her müşteri ve ürün kombinasyonunun sipariş sayısını hesaplayan CTE
    select 
        c.customer_id, 
        od.product_id,
        count(*) as order_count
    from customers c
    -- müşteri ve siparişleri birleştirdim
    inner join orders o on c.customer_id = o.customer_id
    -- sipariş detaylarını birleştirdim
    inner join order_details od on o.order_id = od.order_id
    -- her müşteri ve ürün için gruplayarak sipariş sayısını hesaplıyorum
    group by c.customer_id, od.product_id
    -- 3 veya daha fazla sipariş vermiş olanları alıyorum
    having count(*) >= 3
)
-- müşteri ve ürün bilgilerini almak için CTE ile join yapıyorum
select 
    c.customer_id,
    p.product_name,
    cpc.order_count
from customer_product_counts cpc
inner join customers c on cpc.customer_id = c.customer_id
inner join products p on cpc.product_id = p.product_id


-- 3️) Bir Çalışanın 30 Gün İçinde Verdiği Siparişlerin Bir Önceki 30 Güne Göre Artış/ Azalışını Hesaplayın
--    Her çalışanın (Employees), sipariş sayısının son 30 gün içinde bir önceki 30 güne kıyasla nasıl değiştiğini hesaplayan bir sorgu yazın.
--    Çalışan bazında sipariş sayısı artış/azalış yüzdesi hesaplanmalı. 

select * from employees
select * from orders -- employee_id

with order_count as ( -- Son sipariş tarihinden itibaren 60 gün önceki sipariş vermiş olan müsterileri ve müşterilerin sipariş sayılatını getircek sanal tablo
    select 
        employee_id,
        order_date,
        count(order_id) as order_total
    from orders
	-- orders tablosundan verilmiş son siparişin tarihi yani max(order_date) bulunur.
	-- max(order_date) 'den interval sayeinde 60 gün çıkartarak (60 gün geriye giderek) bir taril oluşturduk.
	-- dolasısıyla bize 60 gün önceden sipariş vermiş olan müşteri ve  siparişlerini getiricek
	-- where den dolayı direk max(order_date) tyazamayız 
    where order_date >= (select max(order_date) from orders) - interval '60 day' 
    group by employee_id, order_date
),

total_orders as (
    select 
        employee_id,
        sum(case when order_date >= (select max(order_date) from orders) - interval '30 day' then order_total else 0 end) as last_30_days,
        sum(case when order_date < (select max(order_date) from orders) - interval '30 day' then order_total else 0 end) as previous_30_days
    from order_count
    group by employee_id
)

select 
    employee_id, 
    last_30_days, 
    previous_30_days,
    case 
        when previous_30_days = 0 then null  -- No orders in the previous 30 days
        else ((last_30_days - previous_30_days) * 100.0 / previous_30_days) 
    end as percentage_change,
    case 
        when last_30_days > previous_30_days then 'Increase'
        when last_30_days < previous_30_days then 'Decrease'
        else 'No Change'
    end as change_type
from total_orders
order by percentage_change desc

-- 4️) Her Müşterinin Siparişlerinde Kullanılan İndirim Oranının Zaman İçinde Nasıl Değiştiğini Bulun
--    Müşterilerin siparişlerinde uygulanan indirim oranlarının zaman içindeki trendini hesaplayan bir sorgu yazın.
--    Müşteri bazında hareketli ortalama indirim oranlarını hesaplayın ve sipariş tarihine göre artış/azalış eğilimi belirleyin.

select * from customers
select * from orders
select * from order_details

-- cte oluşturuluyor: moving_avg_discount adında geçici tablo oluşturuluyor
with moving_avg_discount as (
    select
        o.customer_id,         -- orders tablosundan müşteri id'si
        o.order_date,          -- orders tablosundan sipariş tarihi
        od.discount,           -- order_details tablosundan indirim oranı
        avg(od.discount) over (  -- window function ile hareketli ortalama hesaplanıyor
            partition by o.customer_id   -- her müşteri için ayrı pencere oluşturulur
            order by o.order_date          -- siparişler, sipariş tarihi sırasına göre düzenlenir
            rows between 2 preceding and current row  -- mevcut satır dahil, kendisinden önceki 2 satır alınarak ortalama hesaplanır
        ) as moving_avg_discount  -- hesaplanan hareketli ortalama indirim oranı sütunu
    from orders o
    inner join order_details od on o.order_id = od.order_id  -- orders ile order_details tabloları sipariş id'si üzerinden birleştiriliyor
    group by o.customer_id, o.order_date, od.discount  -- grouping işlemi; window function'ın doğru çalışması için gerekli
)

-- ana sorgu: cte'den veriler alınarak indirim trendi hesaplanıyor
select
    customer_id,           -- cte'den müşteri id'si
    order_date,            -- cte'den sipariş tarihi
    discount,              -- cte'den orijinal indirim oranı
    moving_avg_discount,   -- cte'den hesaplanan hareketli ortalama indirim oranı
    case
        -- bir önceki siparişin hareketli ortalama indirim değerini al (aynı müşteri için)
        when moving_avg_discount > lag(moving_avg_discount) over (partition by customer_id order by order_date)
            then 'increase'  -- eğer mevcut değer önceki değerden büyükse artış var
			-- Lag: ayni sorgudaki satirin bellirli bir araliktaki onceki degerini veriyor
        when moving_avg_discount < lag(moving_avg_discount) over (partition by customer_id order by order_date)
            then 'decrease'  -- eğer mevcut değer önceki değerden küçükse azalış var
			-- Lag: ayni sorgudaki satirin bellirli bir araliktaki onceki degerini veriyor
        else 'no change'      -- aksi durumda değişiklik yok
    end as price_tendency  -- hesaplanan fiyat eğilimi sütunu (trend analizi)
from moving_avg_discount  -- daha önce oluşturulan cte'den veri alınıyor
order by customer_id, order_date;  -- sonuçlar müşteri ve sipariş tarihine göre sıralanıyor