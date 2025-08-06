API_LIB="../javax.servlet-api.jar"

javac -cp $API_LIB -source 1.7 -target 1.7 -d WEB-INF/classes src/TableGenerator.java
jar -cvf table-generator.war WEB-INF/
