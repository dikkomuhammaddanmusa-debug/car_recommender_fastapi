import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { View, Text, Pressable, StyleSheet } from "react-native";
import SearchScreen from "./src/screens/SearchScreen";
import RecommendScreen from "./src/screens/RecommendScreen";
import UploadScreen from "./src/screens/UploadScreen";
import StatsScreen from "./src/screens/StatsScreen";

const Stack = createNativeStackNavigator();

function Home({ navigation }) {
  const Item = ({ label, go }) => (
    <Pressable style={styles.btn} onPress={go}>
      <Text style={styles.btnText}>{label}</Text>
    </Pressable>
  );
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Car Recommender (Mobile)</Text>
      <Item label="Search" go={() => navigation.navigate("Search")} />
      <Item label="Recommend" go={() => navigation.navigate("Recommend")} />
      <Item label="Upload Image" go={() => navigation.navigate("Upload")} />
      <Item label="Stats" go={() => navigation.navigate("Stats")} />
    </View>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={Home} />
        <Stack.Screen name="Search" component={SearchScreen} />
        <Stack.Screen name="Recommend" component={RecommendScreen} />
        <Stack.Screen name="Upload" component={UploadScreen} />
        <Stack.Screen name="Stats" component={StatsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 18, gap: 12, justifyContent: "center" },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 10 },
  btn: { backgroundColor: "#111827", padding: 14, borderRadius: 10 },
  btnText: { color: "white", textAlign: "center", fontSize: 16, fontWeight: "600" },
});
