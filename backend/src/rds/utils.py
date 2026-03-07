from collections import defaultdict
from bs4 import BeautifulSoup
import requests,re
from datetime import datetime
def validate_interval_duration (interval, duration):
    interval = "dd" if interval == "" or interval is None else interval
    duration = 30 if duration == "" or duration is None else duration
    interval_status = False  
    match interval:
        case 'dd' | 'mm' | 'yy':
            interval_status = True
        case _:
            interval_status = False
    
    if interval_status:
        try:
            num = int(duration)
            return True
        except ValueError:
            return False
    else:
        return False

def create_filter(filter_data):
    pass

def clean(s):
    if not s:
        return None
    return re.sub(r"\s+", " ", s.strip())

def extract_table(table, family):
    rows = table.find_all("tr")
    if not rows:
        return []

    headers = [clean(th.text) for th in rows[0].find_all(["th", "td"])]
    norm_headers = [h.lower().replace(" ", "").replace("(", "").replace(")", "") for h in headers]

    results = []

    for row in rows[1:]:
        cells = row.find_all(["th", "td"]) 
        row_cells = []
        for cell in cells:
            colspan = int(cell.get("colspan", 1))
            text = cell.get_text(separator=" ", strip=True)
            row_cells.extend([text] * colspan)

        raw = {headers[i]: clean(row_cells[i]) if i < len(row_cells) else None for i in range(len(headers))}

        record = {
            "rds_hw_type": family,
            "rds_hw_model": None,
            "rds_hw_vcpu": None,
            "rds_hw_core": None,
            "rds_hw_mem": None,
            "rds_hw_storage": None,
            "rds_hw_ebs_gbps": None,
            "rds_hw_ebs_mbps": None,
            "rds_hw_net_gbps": None,
            "url_raw": str(raw),
        }

        for idx, nh in enumerate(norm_headers):
            value = row_cells[idx] if idx < len(row_cells) else None
            if not value:
                continue
            if "model" in nh or "instancesize" in nh or "instancetype" in nh:
                record["rds_hw_model"] = value
            elif "vcpu" in nh:
                record["rds_hw_vcpu"] = value
            elif "core" in nh:
                record["rds_hw_core"] = value
            elif "memory" in nh:
                record["rds_hw_mem"] = value.replace(",", "") if value else None
            elif "storage" in nh:
                record["rds_hw_storage"] = value
            elif "ebs" in nh:
                if "gbps" in nh:
                    record["rds_hw_ebs_gbps"] = value
                else:
                    record["rds_hw_ebs_mbps"] = value
            elif "network" in nh:
                record["rds_hw_net_gbps"] = value
        if record["rds_hw_model"]:
            print(record)
            results.append(record)

    return results

def scrape_rds_instances(url):
    headers = {"User-Agent": "Mozilla/5.0 (professional-scraper)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    final = []

    for header in soup.find_all(["h2", "h3"]):
        family = clean(header.text)
        if any(x in family for x in ["General Purpose", "Memory Optimized", "Compute Optimized", "Why Amazon RDS instances?","Burstable-performance"]):
            continue
        else:
            table = header.find_next("table")
            if table:
                final.extend(extract_table(table, family))
    return final

def extract_ebs_table(table, family):
    family=family.get_text(strip=True)
    rows = table.find_all("tr")
    if not rows:
        return []

    header_elems = table.find("tr").find_all(["th","td"])
    headers = [clean(th.get_text()) for th in header_elems]
    norm_headers = [h.lower().replace(" ", "").replace("(", "").replace(")", "") for h in headers]
  
    results = []
    for row in rows[1:]:
        for sup_tag in row.find_all('sup'):
            sup_tag.decompose()
            
        cells = row.find_all('td')
        raw = {
            headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
            if i < len(cells) else None
            for i in range(len(headers))
        }

        record = {
            "ec2_hw_model": None,
            "ec2_hw_type": family,
            "ec2_hw_basebandwm": None,
            "ec2_hw_maxbandwm": None,
            "ec2_hw_basethroputm": None,
            "ec2_hw_maxthroputm": None,
            "ec2_hw_baseiopsm": None,
            "ec2_hw_maxiopswm": None,
            "url_raw": str(raw),
        }        
        
        if len(cells) <=4:
            record["ec2_hw_model"]=cells[0].get_text(strip=True)
            record["ec2_hw_basebandwm"]=cells[1].get_text(strip=True)
            record["ec2_hw_maxbandwm"]=None
            record["ec2_hw_basethroputm"]=cells[2].get_text(strip=True)
            record["ec2_hw_maxthroputm"]=None
            record["ec2_hw_baseiopsm"]=cells[3].get_text(strip=True)
            record["ec2_hw_maxiopswm"]=None
        
        elif len(cells) >=5:
            record["ec2_hw_model"]=cells[0].get_text(strip=True)
            record["ec2_hw_basebandwm"]=cells[1].get_text(strip=True)
            record["ec2_hw_maxbandwm"]=cells[2].get_text(strip=True)
            record["ec2_hw_basethroputm"]=cells[3].get_text(strip=True)
            record["ec2_hw_maxthroputm"]=cells[4].get_text(strip=True)
            record["ec2_hw_baseiopsm"]=cells[5].get_text(strip=True)
            record["ec2_hw_maxiopswm"]=cells[6].get_text(strip=True)   
                     
        if record["ec2_hw_model"]:
            results.append(record)
 
    return results

def scrape_ebs_instances(url):
    headers = {"User-Agent": "Mozilla/5.0 (professional-scraper)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    final =[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find('div', id='main-col-body')
        h3 = divs.find_all('h3')
        tables = divs.find_all('table')
        i=0
        for table in tables[:-1]:
            final.extend(extract_ebs_table(table, h3[i]))
            i= i+1
    return final

def get_table_rows(table):
    rows = table.find_all('tr')
    return rows

def extract_eol_major_table(table, engine):
    rows = table.find_all('tr')
    results= []
    header_elems = table.find("tr").find_all(["th","td"])
    headers = [clean(th.get_text()) for th in header_elems]
    for row in rows[1:]:
        cells = row.find_all('td')
        raw = {
            headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
            if i < len(cells) else None
            for i in range(len(headers))
        }
        record = {
            "rds_ma_type": engine,
            "rds_ma_ver": cells[0].get_text(strip=True).replace("PostgreSQL",'').replace("Deprecated","").strip(),
            "rds_ma_cm_release_date": cells[1].get_text(strip=True),
            "rds_ma_release_date": cells[2].get_text(strip=True) if engine == "postgres" else cells[5].get_text(strip=True),
            "rds_ma_cm_eol": cells[3].get_text(strip=True) if engine == "postgres" else cells[2].get_text(strip=True),
            "rds_ma_rds_seol": cells[4].get_text(strip=True) if engine == "postgres" else cells[6].get_text(strip=True),
            "rds_ma_ex_eol": cells[7].get_text(strip=True) if engine == "postgres" else cells[9].get_text(strip=True),
            "rds_ma_1y_ex_eol": cells[5].get_text(strip=True) if engine == "postgres" else cells[7].get_text(strip=True),
            "rds_ma_3y_ex_eol" : cells[6].get_text(strip=True) if engine == "postgres" else cells[8].get_text(strip=True),
            "rds_ma_lts" : None if engine == "postgres" else (cells[4].get_text(strip=True).replace("PostgreSQL",'').replace("Aurora ","").strip()),
            "url_raw": str(raw),
            "ma_row_created_at" : datetime.now()
        }     
        results.append(record)
        #print(record)
    return results

def extract_eol_minor_table(table, engine):
    rows = table.find_all('tr')
    results= []
    header_elems = table.find("tr").find_all(["th","td"])
    headers = [clean(th.get_text()) for th in header_elems]
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) <=2:
            pass
        else:
            raw = {
                headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
                if i < len(cells) else None
                for i in range(len(headers))
            }
            record = {
                "rds_mi_type": engine,
                "rds_mi_ma_ver": cells[0].get_text(strip=True).replace("PostgreSQL",'').replace("Deprecated","").replace("*","").replace("(LTS)","").strip().split('.')[0],
                "rds_mi_ver": cells[0].get_text(strip=True).replace("PostgreSQL",'').replace("Deprecated","").replace("*","").replace("(LTS)","").strip(),
                "rds_mi_cr_date": cells[1].get_text(strip=True),
                "rds_mi_release_date": cells[2].get_text(strip=True),
                "rds_mi_seol": cells[3].get_text(strip=True),
                "rds_mi_lts": None if engine == "postgres" else cells[3].get_text(strip=True).replace("PostgreSQL",'').replace("Aurora","").strip(),
                "url_raw": str(raw),
                "mi_row_created_at" : datetime.now()
            }     
            results.append(record)
            #print(record)
    return results

def get_postgres_eol(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    result = {}
    h2_elements = soup.find_all("h2")
    for h2 in h2_elements:
        h2_id = h2.get('id')
        if h2_id =='Release.Calendar':
            content_div = h2.find_next_sibling('div', class_='table-container')
            table = content_div.find("table")
            major = extract_eol_major_table(table, 'postgres')
            result["major"] = major
        elif h2_id =='PostgreSQL.Concepts.VersionMgmt.Supported':
            content_div = h2.find_next_sibling('div', class_='table-container')
            table = content_div.find("table")
            minor = extract_eol_minor_table(table, 'postgres')
            result["minor"] = minor
        else:
            pass
    return result

def get_aurorapg_eol(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    result = {}
    h2_elements = soup.find_all("h2")
    for h2 in h2_elements:
        #print(h2)
        h2_id = h2.get('id')
        if h2_id =='aurorapostgresql.major.versions.supported':
            content_div = h2.find_next_sibling('div', class_='table-container')
            table = content_div.find("table")
            major = extract_eol_major_table(table, 'aurora-postgresql')
            result["major"] = major
        elif h2_id =='aurorapostgresql.minor.versions.supported':
            content_div = h2.find_next_sibling('div', class_='table-container')
            table = content_div.find("table")
            minor =extract_eol_minor_table(table, 'aurora-postgresql')
            result["minor"] = minor
        else:
            pass
    return result


def get_mysql_eol_from_aws(url, etype, engine):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    if engine == "mysql":
        start = soup.find("h2", id="MySQL.Concepts.VersionMgmt.Supported")
        stop = soup.find("h2", id="MySQL.Concepts.VersionMgmt.ReleaseCalendar") 
        tables = []
        if etype == "minor":
            for minortbls in start.next_elements:
                if minortbls == stop:
                    break
                if getattr(minortbls, "name", None) == "table":
                    tables.append(minortbls)  
            minor = extract_eol_mysql_minor_table(tables, engine)
            return minor
            
        elif etype == "major": 
            for minortbls in stop.next_elements:
                if minortbls == stop:
                    break
                if getattr(minortbls, "name", None) == "table":
                    tables.append(minortbls) 
            major=extract_eol_mysql_major_table(tables, 'mysql')
            return major
        else:
            return {}
    else:
        h2_elements = soup.find_all("h2")
        for h2 in h2_elements:
            h2_id = h2.get('id')
            if etype== "major":
                if h2_id =='AuroraMySQL.release-calendars.major':
                    content_div = h2.find_next_sibling('div', class_='table-container')
                    table = content_div.find("table")
                    major = extract_eol_amysql_major_table(table, 'aurora-mysql')
                    return major
            elif etype =="minor":
                if h2_id =='AuroraMySQL.release-calendars.minor' :
                    content_div = h2.find_next_sibling('div', class_='table-container')
                    table = content_div.find("table")
                    minor = extract_eol_amysql_minor_table(table, 'aurora-mysql')
                    return minor
            else:
                pass

def extract_eol_mysql_major_table(tables, engine):
    for table in tables:
        rows = table.find_all('tr')
        results= []
        header_elems = table.find("tr").find_all(["th","td"])
        headers = [clean(th.get_text()) for th in header_elems]
        for row in rows[1:]:
            cells = row.find_all('td')
            raw = {
                headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
                if i < len(cells) else None
                for i in range(len(headers))
            }
            #print(raw)
            record = {
                "rds_ma_type": engine,
                "rds_ma_ver": cells[0].get_text(strip=True).replace("MySQL",'').replace("*","").strip(),
                "rds_ma_cm_release_date": cells[1].get_text(strip=True),
                "rds_ma_release_date": cells[2].get_text(strip=True),
                "rds_ma_cm_eol": cells[3].get_text(strip=True),
                "rds_ma_rds_seol": cells[4].get_text(strip=True),
                "rds_ma_ex_eol": cells[7].get_text(strip=True),
                "rds_ma_1y_ex_eol": cells[5].get_text(strip=True),
                "rds_ma_3y_ex_eol" : cells[6].get_text(strip=True),
                "rds_ma_lts" : None,
                "url_raw": str(raw),
                "ma_row_created_at" : datetime.now()
            }     
            results.append(record)
            #print(record)
    return results


def extract_eol_amysql_major_table(table, engine):
    rows = table.find_all('tr')
    results= []
    header_elems = table.find("tr").find_all(["th","td"])
    headers = [clean(th.get_text()) for th in header_elems]
    for row in rows[1:]:
        cells = row.find_all('td')
        raw = {
            headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
            if i < len(cells) else None
            for i in range(len(headers))
        }
        #print(raw)
        record = {
            "rds_ma_type": engine,
            "rds_ma_ver": cells[0].get_text(strip=True).replace("MySQL",'').replace("(deprecated)","").strip(),
            "rds_ma_cm_release_date": None,
            "rds_ma_release_date": None,
            "rds_ma_cm_eol": cells[2].get_text(strip=True),
            "rds_ma_rds_seol": cells[3].get_text(strip=True),
            "rds_ma_ex_eol": cells[6].get_text(strip=True),
            "rds_ma_1y_ex_eol": cells[4].get_text(strip=True),
            "rds_ma_3y_ex_eol" : cells[5].get_text(strip=True),
            "rds_ma_lts" : cells[1].get_text(strip=True).replace("Aurora MySQL version",'').replace("(deprecated)","").strip(),
            "url_raw": str(raw),
            "ma_row_created_at" : datetime.now()
        }     
        results.append(record)
        #print(record)
    return results

    """
    def get_mysql_minor_eol_from_aws(url, etype, engine):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    result = {}
    h2_elements = soup.find_all("h2")
    for idx, h2 in enumerate(h2_elements):
        h2_id = h2.get('id')
        if etype == "minor":
            if h2_id =='MySQL.Concepts.VersionMgmt.Supported':
                table_containers = h2.find_all_next('div', class_='table-container')
                tables = []
                next_h2 = h2_elements[idx + 1] if idx + 1 < len(h2_elements) else None 
                next_h2_id = next_h2.get('id') if next_h2 else None
                for container in table_containers:
                    if next_h2 and container.find_next('h2', id=next_h2_id):
                        break
                    tables_in_container = container.find_all('table')
                    tables.extend(tables_in_container)
                major = extract_eol_mysql_minor_table(tables, 'aurora-postgresql')
                result["major"] = major
        elif etype == "major": 
            if h2_id =='MySQL.Concepts.VersionMgmt.ReleaseCalendar':
                content_div = h2.find_next_sibling('div', class_='table-container')
                print(content_div)
                table = content_div.find("table")
                minor =extract_eol_mysql_major_table(table, 'mysql')
                #result["minor"] = minor
            pass
        else:
            pass
    return result
    """
def extract_eol_mysql_minor_table(tables, engine):
    results= []
    for table in tables:
        rows = table.find_all('tr')
        header_elems = table.find("tr").find_all(["th","td"])
        headers = [clean(th.get_text()) for th in header_elems]
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) <=2:
                pass
            else:
                raw = {
                    headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
                    if i < len(cells) else None
                    for i in range(len(headers))
                }
                record = {
                    "rds_mi_type": engine,
                    "rds_mi_ma_ver": cells[0].get_text(strip=True).replace("*","").strip(),
                    "rds_mi_ver": cells[0].get_text(strip=True).replace("*","").strip(),
                    "rds_mi_cr_date": cells[1].get_text(strip=True),
                    "rds_mi_release_date": cells[2].get_text(strip=True),
                    "rds_mi_seol": cells[3].get_text(strip=True),
                    "rds_mi_lts": None,
                    "url_raw": str(raw),
                    "mi_row_created_at" : datetime.now()
                }     
                results.append(record)
    return results

def extract_eol_amysql_minor_table(table, engine):
    results= []
    rows = table.find_all('tr')
    header_elems = table.find("tr").find_all(["th","td"])
    headers = [clean(th.get_text()) for th in header_elems]
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) <=2:
            pass
        else:
            raw = {
                headers[i]: clean(cells[i].get_text(separator=" ", strip=True))
                if i < len(cells) else None
                for i in range(len(headers))
            }
            cells[0].find("sup") and cells[0].find("sup").decompose()
            record = {
                "rds_mi_type": engine,
                "rds_mi_ma_ver": re.search(r"\b(\d+)\.\d+", cells[0].get_text(strip=True)).group(1),
                "rds_mi_ver": re.search(r"\b\d+\.\d+\b", cells[0].get_text(strip=True)).group(),
                "rds_mi_cr_date": None,
                "rds_mi_release_date": cells[1].get_text(strip=True),
                "rds_mi_seol": cells[2].get_text(strip=True),
                "rds_mi_lts": re.search(r"MySQL\s+(\d+\.\d+\.\d+)", cells[0].get_text(strip=True)).group(1),
                "url_raw": str(raw),
                "mi_row_created_at" : datetime.now()
            }     
            results.append(record)
    return results

