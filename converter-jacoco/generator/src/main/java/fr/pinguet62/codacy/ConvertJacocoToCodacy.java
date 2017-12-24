package fr.pinguet62.codacy;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.codacy.api.CoverageReport;
import com.codacy.parsers.XMLCoverageParser;
import com.codacy.parsers.implementation.JacocoParser;
import play.api.libs.json.JsValue;
import play.api.libs.json.Json;

import java.io.File;

import static com.codacy.api.Language.withName;
import static play.api.libs.json.Json.toJson;

public class ConvertJacocoToCodacy {

    static class Options {
        @Parameter(names = {"--rootProject"})
        private File rootProject = new File("src/main/java");

        @Parameter(names = {"--reportFile"})
        private File reportFile = new File("target/site/jacoco/jacoco.xml");
    }

    public static void main(String[] args) {
        Options opts = new Options();
        JCommander.newBuilder().addObject(opts).build().parse(args);

        XMLCoverageParser parser = new JacocoParser(withName("Java"), opts.rootProject, opts.reportFile);
        CoverageReport report = parser.generateReport();
        JsValue jsValue = toJson(report, CoverageReport.codacyCoverageReportFmt());

        String json = Json.prettyPrint(jsValue);
        json = json.replaceAll("fr/pinguet62/codacy", "src/main/java/fr/pinguet62/codacy"); // workaround for "rootProject"

        System.out.println(json);
    }

}
