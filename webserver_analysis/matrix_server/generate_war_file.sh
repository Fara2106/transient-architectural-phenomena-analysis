API_LIB="../javax.servlet-api.jar"

javac -cp $API_LIB -source 1.7 -target 1.7 -d WEB-INF/classes src/MatrixMultiplication.java
jar -cvf matrix-multiplication.war WEB-INF/
