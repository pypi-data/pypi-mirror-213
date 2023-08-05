import unittest
import re

from bs4 import BeautifulSoup

from crawlutils.soup_traversal import get_td_text, get_td_value_after, get_td, get_td_regex, get_td_text_regex, \
    find_table, get_td_value


class TestSoupTraversal(unittest.TestCase):

    def test_get_td_regex(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값1</td></tr>
                <tr><td>정정사2</td><td>정정사유값2</td></tr>
                <tr><td>정정사3</td><td>정정사유값3</td></tr>
                <tr><td>정정사4</td><td>정정사유값4</td></tr>
            </table> 
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_regex(soup.select("td"), r'정.*3')
        self.assertEqual('정정사3', r.text)

    def test_get_td_text_regex(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값1</td></tr>
                <tr><td>정정사2</td><td>정정사유값2</td></tr>
                <tr><td>정정사3</td><td>정정사유값3</td></tr>
                <tr><td>정정사4</td><td>정정사유값4</td></tr>
            </table> 
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_text_regex(soup.select("td"), r'정.*3')
        self.assertEqual('정정사유값3', r)

    def test_soup_traversal(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값</td></tr>
            </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_value(soup.select("td"), '정정사유')
        self.assertEqual(r, '정정사유값')


    def test_soup_traversal2(self):
        html = """
            <table>
                <tr><td>정정사유</td><td>정정사유값1</td></tr>
                <tr><td>정정사2</td><td>정정사유값2</td></tr>
                <tr><td>정정사3</td><td>정정사유값3</td></tr>
                <tr><td>정정사4</td><td>정정사유값4</td></tr>
            </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        r = get_td_value(soup.select("td"), '정정사1', '정정사3')
        self.assertEqual('정정사유값3', r)

    def test_get_td_text_after(self):
        html = """
        <table>
          <tr> 
       <td width="124"> <span style="width:124px;font-size:10pt;">계약금액 총액(원)</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;text-align:right;">11,380,800,000</span> </td> 
      </tr> 
      <tr> 
       <td width="124"> <span style="width:124px;font-size:10pt;">최근 매출액(원)</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;text-align:right;">70,440,395,777</span> </td> 
      </tr> 
      <tr> 
       <td width="124"> <span style="width:124px;font-size:10pt;">매출액 대비(%)</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;text-align:right;">16.16</span> </td> 
      </tr> 
      <tr> 
       <td colspan="2" width="268"> <span style="width:268px;font-size:10pt;">3. 계약상대방</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;">-</span> </td> 
      </tr> 
      <tr> 
       <td colspan="2" width="268"> <span style="width:268px;font-size:10pt;">-최근 매출액(원)</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;text-align:right;">1,238,811</span> </td> 
      </tr> 
      <tr> 
       <td colspan="2" width="268"> <span style="width:268px;font-size:10pt;">-주요사업</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;">-</span> </td> 
      </tr> 
      <tr> 
       <td colspan="2" width="268"> <span style="width:268px;font-size:10pt;">-회사와의 관계</span> </td> 
       <td colspan="2" width="332"> <span class="xforms_input" style="width:332px;font-size:10pt;">-</span> </td> 
      </tr> 
      <tr> 
      </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        tds = soup.select("td")
        anchor_td = get_td(tds, "계약상대방")
        r = get_td_value_after(anchor_td, 5, "최근매출액")
        self.assertEqual("1,238,811", r)

    def test_find_table(self):
        html = """
            <table>
                <tr><td>계약내용</td><td>정정사유값</td></tr>
                <tr><td>정정전</td><td>정정사유값</td></tr>
            </table>
            <table>
                <tr><td>계약내용</td><td>125125</td></tr>
            </table>
            <table>
                <tr><td>정 정사</td><td>정정사이값</td></tr>
            </table>
            <table>
                <tr><td>정 정사</td><td>정정사이값</td></tr>
            </table>
        """
        soup = BeautifulSoup(html, "html.parser")
        r = find_table(soup.findAll("table"), contains_any=['계약내용',"기한"], not_contains_any=['정정전', '정정후'])
        self.assertEqual(r, soup.select("table")[1])