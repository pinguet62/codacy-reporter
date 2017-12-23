package fr.pinguet62.codacy;

import com.codacy.api.CoverageReport;
import com.codacy.api.Language;
import com.codacy.parsers.XMLCoverageParser;
import com.codacy.parsers.implementation.JacocoParser;
import play.api.libs.json.JsValue;
import play.api.libs.json.Json;
import scala.Enumeration;

import java.io.File;

import static java.nio.file.Files.write;
import static java.nio.file.Paths.get;
import static play.api.libs.json.Json.toJson;

public class ConvertJacocoToCodacy {

    /**
     * @param args Path to root project.<br>
     *             {@code "jacoco/generator"} if executed on root Git project.
     */
    public static void main(String[] args) throws Exception {
        Enumeration.Value language = Language.withName("Java");
        File rootProject = new File(".");
        File reportFile = new File(args[0], "target/site/jacoco/jacoco.xml");

        XMLCoverageParser parser = new JacocoParser(language, rootProject, reportFile);
        CoverageReport report = parser.generateReport();
        JsValue jsValue = toJson(report, CoverageReport.codacyCoverageReportFmt());

        String json = Json.prettyPrint(jsValue);
        json = json.replaceAll("fr/pinguet62/codacy", "src/main/java/fr/pinguet62/codacy");

        write(get(args[0], "target/site/jacoco/codacy.json"), json.getBytes());
    }

}
