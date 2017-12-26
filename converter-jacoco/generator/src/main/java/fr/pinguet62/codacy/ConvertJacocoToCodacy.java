package fr.pinguet62.codacy;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.codacy.api.CoverageFileReport;
import com.codacy.api.CoverageReport;
import com.codacy.parsers.XMLCoverageParser;
import com.codacy.parsers.implementation.JacocoParser;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.util.List;
import java.util.Map;

import static com.codacy.api.Language.withName;
import static fr.pinguet62.codacy.ConvertJacocoToCodacy.ScalaToJavaModel.toJson;
import static java.util.stream.Collectors.toList;
import static scala.collection.JavaConverters.mapAsJavaMap;
import static scala.collection.JavaConverters.seqAsJavaList;

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

        String json = toJson(report);

        json = json.replaceAll("fr/pinguet62/codacy", "src/main/java/fr/pinguet62/codacy"); // workaround for "rootProject"

        System.out.println(json);
    }

    /**
     * GSON doesn't support natively Scala collection {@link scala.collection.Seq} and {@link scala.collection.Map}: map to Java.
     */
    static class ScalaToJavaModel {
        /**
         * Hard to use "rapture" library: use GSON
         */
        static String toJson(CoverageReport coverageReport) {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            return gson.toJson(new JavaCoverageReport(coverageReport));
        }

        static class JavaCoverageReport {
            final Integer total;
            final List<JavaCoverageFileReport> fileReports;

            JavaCoverageReport(CoverageReport coverageReport) {
                this.total = coverageReport.total();
                fileReports = seqAsJavaList(coverageReport.fileReports()).stream()
                        .map(JavaCoverageFileReport::new)
                        .collect(toList());
            }
        }

        static class JavaCoverageFileReport {
            final String filename;
            final Integer total;
            final Map<Object, Object> coverage;

            JavaCoverageFileReport(CoverageFileReport coverageFileReport) {
                this.filename = coverageFileReport.filename();
                this.total = coverageFileReport.total();
                this.coverage = mapAsJavaMap(coverageFileReport.coverage());
            }
        }
    }

}
