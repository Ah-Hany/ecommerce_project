use("ecommerce_nosql");

db.reviews.aggregate([
  {
    $group: {
      _id: "$product_name",
      avg_rating: { $avg: "$rating" },
      total_reviews: { $sum: 1 }
    }
  },
  {
    $sort: { avg_rating: -1 }
  }
]);

db.user_activity.aggregate([
  {
    $group: {
      _id: "$action",
      total_actions: { $sum: 1 }
    }
  },
  {
    $sort: { total_actions: -1 }
  }
]);

db.user_activity.find({ 
  action: "purchase" 
}).sort({ timestamp: -1 });
