import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Set;

public class Task1 {
    public static void main(String[] args) throws IOException {

        Set<String> urls = new HashSet<>();

        //Собираю ссылки всех страниц
        //Для этого открываю заглавную страницу википедии, где собраны ссылки на другие статьи
        Document doc = Jsoup.connect("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0").get();
        //Далее беру все элементы тега <a> с ссылками
        Elements elems = doc.select("a");

        //Далее в каждом таком элементе вытаскиваю href ссылку и записываю её в список будущих страниц
        for (Element elem : elems) {
            String url = elem.attr("href");

            if (url.contains("https://")) {
                urls.add(url);
            } else if (url.startsWith("/wiki/")) {
                urls.add("https://ru.wikipedia.org" + url);
            }
            //Ограничиваю кол-во страниц до 100 по заданию
            if (urls.size() >= 100) break;
        }

        int i = 0;

        //Создаю файл index.txt
        File index = new File("index.txt");
        index.createNewFile();
        PrintWriter indexWriter = new PrintWriter(index);

        //Прохожусь по всем ссылкам и качаем страницу в файл
        for (String url : urls) {
            String page = Jsoup.connect(url).get().html();

            //Сохраняю скачанный код страницы в файл
            File savedPage = new File("pages/" + i++ + ".txt");
            savedPage.createNewFile();
            PrintWriter pw = new PrintWriter(savedPage);
            pw.println(page);
            pw.flush();
            pw.close();

            //Добавляю запись о файле в index.txt
            indexWriter.println("" + (i-1) + " " + url);
        }

        indexWriter.flush();
        indexWriter.close();
    }
}
