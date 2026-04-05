using System;
using System.Collections.Generic;
using System.Formats.Asn1;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Xml;
using System.Xml.Linq;
using CsvHelper;
using HtmlAgilityPack;
using Microsoft.VisualBasic;

class csvData {
    public string? nameRU { get; set; }
    public string? nameEN { get; set; }
    public string? imgSrc { get; set; }
    public string? descr { get; set; }
    public string? imgName { get; set; }
    public string? reloadCnt { get; set; }
    public string? urlToPage { get; set; } //site page
    public Boolean? isPassive { get; set; }
    public Boolean? isWrath { get; set; } //addon
    public Boolean? isTrinket { get; set; }
}

class Program
{
    static void Log(string url, string text)
    {
        File.AppendAllText("log.txt", $"{url}\t{text}\n");
    }

    static List<csvData> TableParse(HtmlNode tableNode, int rowLimit, Boolean isReloadColumnExist)
    {
        var items = new List<csvData>();

        var rows = tableNode.SelectNodes(".//tr")?.Skip(1) ?? Enumerable.Empty<HtmlNode>();

        Console.WriteLine("--itemCnt " + rows.Count());

        int i = 0;

        var nameRUXpath = ".//td[1]//a";
        var nameENXpath = ".//td[2]";
        var imgSrcXpath = ".//td[1]//img";
        var descrXpath = ".//td[3]";        
        var reloadCntXpath = ".//td[4]";
        //trinkets
        imgSrcXpath = ".//td[3]//img";
        descrXpath = ".//td[4]";
        foreach (var tr in rows)
        {
            if (i == rowLimit)
                break;

            var nameNode = tr.SelectSingleNode(nameRUXpath);
            var nameRU = nameNode?.InnerText.Trim() ?? "";
            var urlToPage = nameNode?.GetAttributeValue("href", "")?.Trim() ?? "";

            Console.WriteLine($"{i} {nameRU}");

            var nameEN = tr.SelectSingleNode(nameENXpath)?.InnerText.Trim() ?? "";

            var imgSrc = tr.SelectSingleNode(imgSrcXpath)
                ?.GetAttributeValue("src", "")?.Trim() ?? "";//src data-src

            var descr = tr.SelectSingleNode(descrXpath)?.InnerText.Trim() ?? "";

            var reload = "";
            if (isReloadColumnExist){
                reload = tr.SelectSingleNode(reloadCntXpath)?.InnerText.Trim() ?? "";
            }
            
            var imgArray = imgSrc.Split('/');
            string imgName = imgArray.First(x => x.Contains(".png") || x.Contains(".webp"));

            reload = "-1";
           
            items.Add(new csvData
            {
                nameRU = nameRU,
                nameEN = nameEN,
                imgSrc = imgSrc,
                descr = descr,
                imgName = imgName,
                reloadCnt = reload,
                urlToPage = urlToPage
            }
            );

            i++;
        }

        return items;
    }

    static void WriteCsv(string path, List<csvData> items)
    {

        using var writer = new StreamWriter(path, false, new UTF8Encoding(false));
        /*
        foreach (csvData row in items)
        {
            writer.WriteLine(string.Join(",", extendedRow.Select(v => $"\"{v.Replace("\"", "\"\"")}\"")));
        }
        */
        using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
        {
            csv.WriteRecords(items);
        }
    }

    static void Main()
    {
        var filePath = "./ALL/Артефакты (Flash) _ The Binding of Isaac вики _ Fandom.HTML";
        filePath = @"E:\OneDrive\_workflow\binding of issac FLASH item description\parseHTML\ALL\Артефакты (Flash) _ The Binding of Isaac вики _ Fandom.HTML";
        filePath = @"E:\OneDrive\_workflow\binding of issac FLASH item description\parseHTML\ALL\Брелоки (Flash) _ The Binding of Isaac вики _ Fandom.html";

        var text = File.ReadAllText(filePath, Encoding.UTF8);

        var doc = new HtmlDocument();
        doc.LoadHtml(text);

        var tables = doc.DocumentNode.SelectNodes("//table[@class]");

        if (tables == null || tables.Count < 2)//3
        {
            Console.WriteLine("Tables not found");
            return;
        }
        /*
        var isPassive = false;
        var isWrath = false;
        var items1 = TableParse(tables[0],rowLimit: 35,isReloadColumnExist: true); //Активируемые артефакты / перезарядки
        for (int i = 0; i < items1.Count; i++)
        {
            items1[i].isPassive = isPassive;
            items1[i].isWrath = isWrath;
            items1[i].isTrinket = isTrinket;
        }
        WriteCsv("1.csv", items1);

        isPassive = true;
        isWrath = false;
        var items2 = TableParse(tables[1],rowLimit: -1,isReloadColumnExist: false); //Пассивные артефакты
                for (int i = 0; i < items2.Count; i++)
        {
            items2[i].isPassive = isPassive;
            items2[i].isWrath = isWrath;
            items2[i].isTrinket = isTrinket;
        }
        WriteCsv("2.csv", items2);

        isPassive = false;
        isWrath = true;
        var items3 = TableParse(tables[2],rowLimit: -1,isReloadColumnExist: true); //Активируемые артефакты (Wrath of the Lamb / перезарядки
                for (int i = 0; i < items3.Count; i++)
        {
            items3[i].isPassive = isPassive;
            items3[i].isWrath = isWrath;
            items3[i].isTrinket = isTrinket;
        }
        WriteCsv("3.csv", items3); 

        isPassive = true;
        isWrath = true;
        var items4 = TableParse(tables[3],rowLimit: -1,isReloadColumnExist: false); //Пассивные артефакты(Wrath of the Lamb
                for (int i = 0; i < items4.Count; i++)
        {
            items4[i].isPassive = isPassive;
            items4[i].isWrath = isWrath;
            items4[i].isTrinket = isTrinket;
        }
        WriteCsv("4.csv", items4);
        */
        var isPassive = true;  
        var isWrath = true;
        var isTrinket = true;
        var items5= TableParse(tables[0], rowLimit: -1, isReloadColumnExist: false); //брелоки (Wrath of the Lamb
        for (int i = 0; i < items5.Count; i++)
        {
            items5[i].isPassive = isPassive;
            items5[i].isWrath = isWrath;
            items5[i].isTrinket = isTrinket;
        }
        WriteCsv("5.csv", items5);
    }
}