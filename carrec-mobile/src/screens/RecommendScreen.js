import React, { useState } from "react";
import { View, Text, TextInput, Pressable, FlatList, StyleSheet } from "react-native";
import { recommendCars } from "../api";

export default function RecommendScreen() {
  const [brand, setBrand] = useState("Toyota");
  const [minYear, setMinYear] = useState("2018");
  const [topK, setTopK] = useState("5");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);

  const go = async () => {
    setLoading(true);
    try {
      const body = {
        filters: { brand: brand || undefined, min_year: minYear ? Number(minYear) : undefined },
        top_k: topK ? Number(topK) : 5,
        weights: { year: 0.5, price: 0.3, mileage: 0.2 },
      };
      const { data } = await recommendCars(body);
      setRows(data);
    } catch (e) {
      console.warn(e?.response?.data || e.message);
    } finally {
      setLoading(false);
    }
  };

  const Item = ({ item }) => (
    <View style={styles.card}>
      <Text style={styles.title}>
        {item.brand}{item.model ? ` – ${item.model}` : ""}
      </Text>
      <Text>Year: {item.year ?? "-"}</Text>
      <Text>Price: {item.price ?? "-"}</Text>
      <Text>Mileage: {item.mileage ?? "-"}</Text>
      <Text>Transmission: {item.transmission ?? "-"}</Text>
      <Text>Fuel: {item.fuel ?? "-"}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Top-K Recommendations</Text>
      <View style={styles.row}>
        <TextInput style={styles.input} placeholder="Brand" value={brand} onChangeText={setBrand} />
        <TextInput style={styles.input} placeholder="Min Year" value={minYear} onChangeText={setMinYear} keyboardType="number-pad" />
      </View>
      <View style={styles.row}>
        <TextInput style={styles.input} placeholder="Top K (default 5)" value={topK} onChangeText={setTopK} keyboardType="number-pad" />
      </View>
      <Pressable style={styles.btn} onPress={go} disabled={loading}>
        <Text style={styles.btnText}>{loading ? "Recommending..." : "Recommend"}</Text>
      </Pressable>

      <FlatList
        data={rows}
        keyExtractor={(x, i) => String(x.id ?? i)}
        renderItem={Item}
        style={{ marginTop: 10 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 14 },
  h1: { fontSize: 20, fontWeight: "700", marginBottom: 10 },
  row: { flexDirection: "row", gap: 10, marginBottom: 10 },
  input: { flex: 1, borderWidth: 1, borderColor: "#ddd", padding: 10, borderRadius: 8 },
  btn: { backgroundColor: "#111827", padding: 12, borderRadius: 8, marginTop: 6 },
  btnText: { color: "white", textAlign: "center", fontWeight: "600" },
  card: { padding: 12, borderWidth: 1, borderColor: "#eee", borderRadius: 10, marginBottom: 10 },
  title: { fontWeight: "700", marginBottom: 4 },
});
