import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from "react-native";
import { searchCars } from "../src/api";

export default function Search() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    (async () => {
      try {
        const res = await searchCars({ limit: 10 });
        setData(res.data || []);
      } catch (e) {
        console.warn("searchCars error", e?.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);
  if (loading) return <ActivityIndicator style={{ marginTop: 40 }} />;
  return (
    <View style={styles.wrap}>
      <Text style={styles.title}>Search Results</Text>
      <FlatList
        data={data}
        keyExtractor={(item, idx) => String(item.id ?? idx)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.display_name || `${item.brand} ${item.model}`}</Text>
            <Text>Year: {item.year}</Text>
            <Text>Price: {item.price}</Text>
            <Text>Mileage: {item.mileage}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, padding: 16 },
  title: { fontSize: 18, fontWeight: "700", marginBottom: 12 },
  card: { padding: 12, borderWidth: 1, borderColor: "#ddd", borderRadius: 8, marginBottom: 10 },
  name: { fontWeight: "700", marginBottom: 4 },
});
